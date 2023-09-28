from django_filters import FilterSet, DateFromToRangeFilter  # импортируем filterset, чем-то напоминающий знакомые дженерики
from .models import Post


# создаём фильтр
class PostFilter(FilterSet):
    data_time = DateFromToRangeFilter(field_name='data_time', label='Дата публикации')
    # Здесь в мета классе надо предоставить модель и указать поля, по которым будет фильтроваться (т. е. подбираться) информация о товарах
    class Meta:
        model = Post
        fields = ('title_post', 'text_post', 'author',
                  'post_category')  # поля, которые мы будем фильтровать (т. е. отбирать по каким-то критериям, имена берутся из моделей)