from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Post(models.Model):
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    type = models.ForeignKey('Type', on_delete=models.CASCADE, verbose_name='Тип')
    content = models.TextField(verbose_name='Содержание')
    rating = models.IntegerField(blank=True, null=True, verbose_name='Рейтинг')
    price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True, verbose_name='Цена')
    map = models.TextField(blank=True, null=True, verbose_name='Код карты')
    date_posted = models.DateTimeField(default=timezone.now, verbose_name='Дата публикации')
    date_updated = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
    image = models.ImageField(upload_to='post_pics', blank=True, null=True, verbose_name='Изображение')
    likes = models.ManyToManyField(User, blank=True, related_name='likes', verbose_name='Лайки')
    
    class Meta:
        ordering = ['title']
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'

    def get_absolute_url(self):
        return f'/post/{self.id}'
    
    def like(self, user):
        if user in self.likes.all():
            self.likes.remove(user)
        else:
            self.likes.add(user)

    def likes_count(self):
        return self.likes.count()
    
    @property
    def next_post(self):
        return self.__class__.objects.filter(date_posted__gt=self.date_posted, type=self.type).order_by('date_posted').first()

    @property
    def prev_post(self):
        return self.__class__.objects.filter(date_posted__lt=self.date_posted, type=self.type).order_by('-date_posted').first()

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
    
class Banner(models.Model):
    title = models.CharField(max_length=100, verbose_name='Заголовок', blank=True, null=True)
    image = models.ImageField(upload_to='banners', verbose_name='Изображение')
    description = models.TextField(verbose_name='Описание', blank=True, null=True)

    class Meta:
        verbose_name = 'Баннер'
        verbose_name_plural = 'Баннеры'

    def __str__(self):
        return self.title if self.title else self.image.name.split('/')[-1]