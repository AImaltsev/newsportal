from django.contrib import admin
from .models import Category, Post, PostCategory
from modeltranslation.admin import TranslationAdmin # импортируем модель амдинки (вспоминаем модуль про переопределение стандартных админ-инструментов)

admin.site.register(Category)

class PostCategoryInline(admin.TabularInline):
    model = PostCategory

class PostAdmin(admin.ModelAdmin):
    list_display = ('title_post', 'author', 'get_categories')
    inlines = [PostCategoryInline]  # Добавляем связанные категории как инлайн

    def get_categories(self, obj):
        return ", ".join([c.category.category_name for c in obj.postcategory_set.all()])

    get_categories.short_description = 'Категории'

admin.site.register(Post, PostAdmin)


class CategoryAdmin(TranslationAdmin):
    model = Category

class PostAdmin(TranslationAdmin):
    model = Post