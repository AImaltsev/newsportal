from django.contrib.auth.models import User
from django.db import models
from django.db.models import Sum
from django.db.models.functions import Coalesce


article = 'AR'
news = 'NE'

choices = [
    (article, 'Cтатья'),
    (news, 'Новость'),
]
# Модель, содержащая объекты всех авторов.
# Имеет следующие поля:
# связь «один к одному» с встроенной моделью пользователей User;
# рейтинг пользователя. Ниже будет дано описание того, как этот рейтинг можно посчитать.
class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating_author = models.IntegerField(default=0)

    def update_rating(self):
        author_post_rating = Post.objects.filter(author_id=self.pk).aggregate(
            post_rating_sum=Coalesce(Sum('rating_post') * 3, 0))
        author_comment_rating = Comment.objects.filter(user_id=self.user).aggregate(
            comments_rating_sum=Coalesce(Sum('rating_comment'), 0))
        author_post_comment_rating = Comment.objects.filter(post__author__name=self.user).aggregate(
            comments_rating_sum=Coalesce(Sum('rating_comment'), 0))
        self.rating_author = author_post_rating['post_rating_sum'] + author_comment_rating['comments_rating_sum'] + author_post_comment_rating['comments_rating_sum']
        self.save()




# Категории новостей/статей — темы, которые они отражают (спорт, политика, образование и т. д.).
# Имеет единственное поле: название категории.
# Поле должно быть уникальным (в определении поля необходимо написать параметр unique = True).
class Category(models.Model):
    category_name = models.CharField(max_length=100, unique=True)


# Эта модель должна содержать в себе статьи и новости, которые создают пользователи.
# Каждый объект может иметь одну или несколько категорий.
# Соответственно, модель должна включать следующие поля:
# связь «один ко многим» с моделью Author;
# поле с выбором — «статья» или «новость»;
# автоматически добавляемая дата и время создания;
# связь «многие ко многим» с моделью Category (с дополнительной моделью PostCategory);
# заголовок статьи/новости;
# текст статьи/новости;
# рейтинг статьи/новости.



class Post(models.Model):
    type_post = models.CharField(max_length=10, choices=choices)
    data_time = models.DateTimeField(auto_now_add=True)
    post_category = models.ManyToManyField(Category, through='PostCategory')
    title_post = models.CharField(max_length=255)
    text_post = models.TextField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    rating = models.FloatField()

    def like(self):
        self.rating += 1

    def dislike(self):
        self.rating -= 1

    def preview(self):
        if len(self.text_post) > 124:
            return self.text_post[:124] + '...'
        else:
            return self.text_post


# Промежуточная модель для связи «многие ко многим»:
# связь «один ко многим» с моделью Post;
# связь «один ко многим» с моделью Category.
class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


# Под каждой новостью/статьёй можно оставлять комментарии, поэтому необходимо организовать их способ хранения тоже.
# Модель будет иметь следующие поля:
# связь «один ко многим» с моделью Post;
# связь «один ко многим» со встроенной моделью User (комментарии может оставить любой пользователь,
# необязательно автор);
# текст комментария;
# дата и время создания комментария;
# рейтинг комментария.
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text_comment = models.TextField()
    data_time = models.DateTimeField(auto_now_add=True)
    rating = models.FloatField(default=0)

    def like(self):
        self.rating += 1

    def dislike(self):
        self.rating -= 1
