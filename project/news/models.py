from django.contrib.auth.models import User
from django.db import models


# Модель, содержащая объекты всех авторов.
# Имеет следующие поля:
# связь «один к одному» с встроенной моделью пользователей User;
# рейтинг пользователя. Ниже будет дано описание того, как этот рейтинг можно посчитать.
class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating_user = models.FloatField(default=0)

    def update_rating(self):
        post_rating = self.post_set.aggregate(sum('rating_post'))['rating_post__sum'] or 0
        comment_rating = self.comment_set.aggregate(sum('rating_comment'))['rating_comment__sum'] or 0

        self.rating_user = (post_rating * 3) + comment_rating
        self.save()



# Категории новостей/статей — темы, которые они отражают (спорт, политика, образование и т. д.).
# Имеет единственное поле: название категории.
# Поле должно быть уникальным (в определении поля необходимо написать параметр unique = True).
class Category(models.Model):
    category_name = models.CharField(unique=True)


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
article = 'article'
news = 'news'
choices = [
    (article, 'статья'),
    (news, 'новость'),
]


class Post(models.Model):
    author_post = models.OneToOneField(Author, on_delete=models.CASCADE)
    type_post = models.CharField(max_length=10, choices=choices)
    data_time = models.DateTimeField(auto_now_add=True)
    post_category = models.ManyToManyField(Category, through='PostCategory')
    title_post = models.CharField()
    text_post = models.TextField()
    rating_post = models.FloatField()

    def like(self):
        self.rating_post += 1

    def dislike(self):
        self.rating_post -= 1

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
    rating_comment = models.FloatField(default=0)

    def like(self):
        self.rating_comment += 1

    def dislike(self):
        self.rating_comment -= 1
