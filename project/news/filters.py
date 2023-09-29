from django import forms
from django_filters import FilterSet, DateFilter
from .models import Post

# создаём фильтр
class PostFilter(FilterSet):
    data_time__gte = DateFilter(
        field_name='data_time',
        label='Дата публикации (позже чем)',
        widget=forms.DateInput(attrs={'type': 'date'}),
        lookup_expr='gt',  # Используйте 'gte' для больше или равно
        exclude=True,  # Исключите точное совпадение с указанной датой
    )
    class Meta:
        model = Post
        fields = {
            'title_post' : ['icontains'],
            'text_post' : ['icontains'],
            'author' : ['exact'],
            'post_category' : ['exact']
        }  # поля, которые мы будем фильтровать (т. е. отбирать по каким-то критериям, имена берутся из моделей)