from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Post(models.Model):
    title = models.CharField(max_length=100, verbose_name='Заголовок')
    type = models.ForeignKey('Type', on_delete=models.CASCADE, verbose_name='Тип')
    content = models.TextField(verbose_name='Содержание')
    rating = models.IntegerField(blank=True, null=True, verbose_name='Рейтинг')
    price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True, verbose_name='Цена')
    date_posted = models.DateTimeField(default=timezone.now, verbose_name='Дата публикации')
    date_updated = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
    image = models.ImageField(upload_to='upload/post_pics', blank=True, null=True, verbose_name='Изображение')

    class Meta:
        ordering = ['title']
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'

    def get_absolute_url(self):
        return f'/post/{self.id}'

    def next_post(self):
        return Post.objects.filter(date_posted__gt=self.date_posted, type=self.type).order_by('date_posted').first()

    def prev_post(self):
        return Post.objects.filter(date_posted__lt=self.date_posted, type=self.type).order_by('-date_posted').first()

    def __str__(self):
        return self.title

class Type(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')
    plural = models.CharField(max_length=100, blank=True, null=True, verbose_name='Множественное число')

    class Meta:
        ordering = ['name']
        verbose_name = 'Тип'
        verbose_name_plural = 'Типы'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.plural:
            self.plural = self.name
        super().save(*args, **kwargs)

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name='Пост')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
    content = models.TextField(verbose_name='Содержание')
    date_posted = models.DateTimeField(default=timezone.now, verbose_name='Дата публикации')

    class Meta:
        ordering = ['date_posted']
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.content
