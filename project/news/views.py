from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Post
from datetime import datetime


class PostsList(ListView):
    model = Post
    template_name = 'posts.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return Post.objects.order_by('-data_time')

    def get_context_data(self, **kwargs):
        # С помощью super() мы обращаемся к родительским классам
        # и вызываем у них метод get_context_data с теми же аргументами,
        # что и были переданы нам.
        # В ответе мы должны получить словарь.
        context = super().get_context_data(**kwargs)
        # К словарю добавим текущую дату в ключ 'time_now'.
        context['time_now'] = datetime.utcnow()
        return context


class PostViews(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'

