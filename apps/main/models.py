import uuid

from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


# Create your models here.
# ORM - object relation model

# create table if not exists

# Model

# create table if not exists main_category (
#   id INTEGER PRIMARY KEY .....,
#   name TEXT
# );

# VARCHAR(20)


class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False,
                          verbose_name='АЙДИ')
    name = models.CharField(max_length=60, verbose_name='Название')

    def __str__(self):
        return self.name

    # добавить категория
    class Meta:  # класс для дополнительных настроек таблицы
        verbose_name = 'Категория'  # название данной модели на русском в единственном числе
        verbose_name_plural = 'Категории'  # название данной модели на русском во множественном числе


# python manage.py makemigrations
# python manage.py migrate


# создать модель FAQ
# id
# question CharField
# answer TextField

class FAQ(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False,
                          verbose_name='АЙДИ')
    question = models.CharField(verbose_name='Вопрос', max_length=100)
    answer = models.TextField(verbose_name='Ответ')

    def __str__(self):
        return self.question

    class Meta:
        verbose_name = 'Вопрос-ответ'
        verbose_name_plural = 'Вопросы-ответы'


class Article(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False,
                          verbose_name='АЙДИ')
    title = models.CharField(max_length=100, verbose_name='Название')
    short_description = models.TextField(verbose_name='Краткое описание')
    full_description = models.TextField(blank=True, null=True, verbose_name='Полное описание')
    views = models.IntegerField(default=0, verbose_name='Кол-во просмотров')
    is_active = models.BooleanField(default=True, verbose_name='Активна ли статья?')
    image = models.ImageField(upload_to='articles/previews/', null=True, blank=True, verbose_name='Заставка')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата и время обновления')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')

    def get_absolute_url(self):
        return reverse('article-page', kwargs={'article_id': self.id})

    def get_detail_info(self):
        return {
            'total views': self.views,
            'category': self.category.name,
            'author': self.author.username,
            'total comments': self.comment_set.all().count(),
            'total likes': self.likes.user.all().count(),
            'total dislikes': self.dislikes.user.all().count(),
            'created at': self.created_at
        }

    def __str__(self):
        return self.title

    def get_image(self):
        if self.image:
            return self.image.url
        return 'https://olmeko.ru/upload/iblock/2e0/net-kartinki.jpg'

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'


# отобразить данную модель в админ панели
# добавить по 1 статье на категорию в админ панели
# попробовать отобразить статьи на главной странице
# 1) внутри функции главной страницы получить все статьи из модели Article
# 2) полученные статьи отдать в context
# 3) в index.html - сделать цикл по ключу из context

# title
# short_description
# full_description
# views
# image
# is_active
# created_at
# updated_at
# category
# author

# создать модель Comment
# author, text, created_at
# добавить модель в админку

class Comment(models.Model):
    text = models.TextField(verbose_name='Комментарий')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
    article = models.ForeignKey(Article, on_delete=models.CASCADE, verbose_name='Статья', null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    def __str__(self):
        return f'{self.text}'[:100] + '...'

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'


# создать класс для формы комментария
# text forms.Textarea

# article.comments.all()
# article.articleimage_set.all()
# article.images.all()

def make_article_image_path(instance, filename):
    return f'articles/gallery/{instance.article.id}/{filename}'


class ArticleImage(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='images', verbose_name='Статья')
    image = models.ImageField(upload_to=make_article_image_path, verbose_name='Фото')


class Like(models.Model):
    article = models.OneToOneField(Article, on_delete=models.CASCADE, related_name='likes')
    user = models.ManyToManyField(User, related_name='likes')


class Dislike(models.Model):
    article = models.OneToOneField(Article, on_delete=models.CASCADE, related_name='dislikes')
    user = models.ManyToManyField(User, related_name='dislikes')


class ArticleViewsCount(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
