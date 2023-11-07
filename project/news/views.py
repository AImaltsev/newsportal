from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from .models import Post, Category, Author, User
from datetime import datetime, timedelta
from django.views import View
from django.core.paginator import Paginator
from .filters import PostFilter
from django.core.mail import send_mail
from .forms import PostForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib import messages
from django.template.loader import render_to_string
from django.utils.translation import gettext as _


class Index(View):
    def get(self, request):
        string = _('Hello world')

        return HttpResponse(string)

class PostsList(ListView):
    model = Post
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        # Получаем отфильтрованный queryset с помощью фильтра
        queryset = PostFilter(self.request.GET, queryset=Post.objects.all()).qs
        return queryset.order_by('-data_time')  # Сортируем по убыванию даты

    def get_context_data(self,
                         **kwargs):  # забираем отфильтрованные объекты переопределяя метод get_context_data у наследуемого класса (привет, полиморфизм, мы скучали!!!)
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET,
                                       queryset=self.get_queryset())  # вписываем наш фильтр в контекст
        context['categories'] = Category.objects.all()
        context['form'] = PostForm()
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)  # создаём новую форму, забиваем в неё данные из POST-запроса

        if form.is_valid():  # если пользователь ввёл всё правильно и нигде не ошибся, то сохраняем новый товар
            form.save()

        return super().get(request, *args, **kwargs)


class PostViews(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'
    queryset = Post.objects.all()


class Search(ListView):
    model = Post
    template_name = 'search.html'
    context_object_name = 'search'
    ordering = ['-data_time']

    def get_context_data(self,
                         **kwargs):  # забираем отфильтрованные объекты переопределяя метод get_context_data у наследуемого класса (привет, полиморфизм, мы скучали!!!)
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET,
                                       queryset=self.get_queryset())  # вписываем наш фильтр в контекст
        return context


class PostCreateView(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    permission_required = 'news.add_post'
    template_name = 'create.html'
    form_class = PostForm

    def form_valid(self, form):
        user = self.request.user
        if isinstance(user, User):
            # Проверка на количество записей пользователя за сутки
            today = datetime.now().date()
            posts_created_today = Post.objects.filter(author__user=user, data_time__date=today).count()

            if posts_created_today >= 10:
                messages.error(self.request, 'Вы превысили лимит на создание записей сегодня.')
                return self.render_to_response(self.get_context_data(form=form))

            # Создаем или получаем автора
            author, created = Author.objects.get_or_create(user=user, defaults={'rating': 0})

            # Присваиваем автора посту
            post = form.save(commit=False)
            post.author = author

            # Получаем категории из формы и присваиваем их посту
            categories = form.cleaned_data.get('post_category')
            post.save()
            post.post_category.set(categories)

            # Отправляем уведомления подписчикам
            post.send_subscription_emails()

            messages.success(self.request, 'Пост успешно создан.')
            return redirect('posts')

        else:
            messages.error(self.request, 'Произошла ошибка при создании поста.')
            return self.render_to_response(self.get_context_data(form=form))

    def form_invalid(self, form):
        messages.error(self.request, 'Произошла ошибка при создании поста.')
        return self.render_to_response(self.get_context_data(form=form))


# дженерик для редактирования объекта
class PostUpdateView(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    permission_required = 'news.change_post'
    template_name = 'edit.html'
    form_class = PostForm


    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


# дженерик для удаления товара
class PostDeleteView(DeleteView):
    template_name = 'post_delete.html'
    queryset = Post.objects.all()
    success_url = '/news/'


def subscribe_to_category(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    category = post.post_category.first()  # Получаем категорию, связанную с постом

    if request.user in category.subscribers.all():
        category.subscribers.remove(request.user)
        messages.success(request, f'Вы успешно отписались от категории "{category.category_name}".')
    else:
        category.subscribers.add(request.user)
        messages.success(request, f'Вы успешно подписались на категорию "{category.category_name}".')

    return redirect(request.META.get('HTTP_REFERER'))




