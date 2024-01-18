from django.db import models
from django.conf import settings
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator

from accounts.models import CustomUser #カスタムユーザー
import os
from datetime import datetime
import hashlib
from django.urls import reverse


def _movie_upload_to(instance, filename):
    current_time = datetime.now()
    pre_hash_name = '%s%s%s' % (instance.id, filename, current_time)
    extension = str(filename).split('.')[-1]
    hs_filename = '%s.%s' % (hashlib.md5(
        pre_hash_name.encode()).hexdigest(), extension)
    saved_path = 'Users/ProfileImages/'
    return '%s%s' % (saved_path, hs_filename)

class Category(models.Model):
    name = models.CharField('カテゴリー', max_length=20)
    category = models.SlugField('タグ', max_length=20)

    def __str__(self):
        return f'{self.name} | {self.category}'

    class Meta:
        verbose_name = "カテゴリー一覧"
        verbose_name_plural = "カテゴリー一覧"

class Tag(models.Model):
    name = models.CharField('名前', max_length=20)
    tag = models.SlugField('タグ', max_length=20)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name} | {self.tag}'
    
    class Meta:
        verbose_name = "タグ一覧"
        verbose_name_plural = "タグ一覧"

class Image(models.Model):
    orderby = models.IntegerField("順番", default=1)
    image = models.ImageField('イメージ画像', upload_to='products_images')
    
    def __str__(self):
        return f'{self.image.name} {self.orderby}'

    class Meta:
        verbose_name = "画像一覧"
        verbose_name_plural = "画像一覧"

class UrlList(models.Model):
    orderby = models.IntegerField("順番", default=1)
    url = models.URLField('URL', blank=False, null=False)
    title = models.CharField('タイトル', blank=False, null=False, max_length=255, default=url)

    def __str__(self):
        return f'{self.orderby} | {self.title} | {self.url}'

    class Meta:
        verbose_name = "URL一覧"
        verbose_name_plural = "URL一覧"

def databaseCount():
    return CreateItem.objects.count()

class CreateItem(models.Model):
    slug = models.SlugField('固有ID')
    orderby = models.IntegerField("順番", default=databaseCount)
    title = models.CharField('タイトル', max_length=100)
    description = models.TextField('商品説明')
    tags = models.ManyToManyField(Tag, related_name='tags', blank=True)
    categories = models.ManyToManyField(Category, related_name='categories', blank=True)
    image = models.ManyToManyField(Image, related_name='images', blank=True)
    # image = models.ForeignKey(Image, related_name='images', blank=True, default="" ,on_delete=models.CASCADE)
    movie = models.FileField(
        upload_to=_movie_upload_to,
        verbose_name='動画ファイル',
        blank=True, null=True
    )
    url = models.ManyToManyField(UrlList, related_name='urls', blank=True)
    pdf = models.FileField("PDF", blank=True, null=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.orderby} {self.title}"
    
    class Meta:
        verbose_name = "成果物一覧"
        verbose_name_plural = "成果物一覧"


class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField("タイトル", max_length=200)
    content = models.TextField("本文")
    created = models.DateTimeField("作成日", default=timezone.now)

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "投稿一覧"
        verbose_name_plural = "投稿一覧"