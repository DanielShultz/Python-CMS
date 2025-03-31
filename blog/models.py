from django.contrib import admin
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

class Type(models.Model):
    """Модель типов постов с возможностью множественной принадлежности"""
    name = models.CharField(max_length=100, verbose_name='Название')
    plural = models.CharField(
        max_length=100, 
        blank=True, 
        null=True, 
        verbose_name='Множественное число',
        help_text='Используется для отображения во множественном числе'
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name='Описание типа'
    )

    class Meta:
        verbose_name = 'Тип'
        verbose_name_plural = 'Типы'
        ordering = ['name']

    def __str__(self):
        return self.name

    @property
    def display_name(self):
        """Возвращает название во множественном числе, если оно задано"""
        return self.plural or self.name

class PostQuerySet(models.QuerySet):
    def with_avg_rating(self):
        return self.annotate(
            avg_rating=Avg('ratings__value')
        )

class Post(models.Model):
    """Основная модель поста с расширенными возможностями"""
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    types = models.ManyToManyField(
        Type,
        related_name='posts',
        verbose_name='Типы',
        help_text='Выберите один или несколько типов для этого поста'
    )
    content = models.TextField(verbose_name='Содержание')
    price = models.DecimalField(
        max_digits=8, 
        decimal_places=2, 
        blank=True, 
        null=True, 
        verbose_name='Цена'
    )
    map = models.TextField(
        blank=True, 
        null=True, 
        verbose_name='Код карты',
        help_text='HTML-код для встраивания карты'
    )
    date_posted = models.DateTimeField(
        default=timezone.now, 
        verbose_name='Дата публикации'
    )
    date_updated = models.DateTimeField(
        auto_now=True, 
        verbose_name='Дата обновления'
    )
    author = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        verbose_name='Автор'
    )
    image = models.ImageField(
        upload_to='post_pics/%Y/%m/%d/', 
        blank=True, 
        null=True, 
        verbose_name='Изображение'
    )
    likes = models.ManyToManyField(
        User, 
        blank=True, 
        related_name='liked_posts',
        verbose_name='Лайки'
    )

    class Meta:
        ordering = ['-date_posted']
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
        indexes = [
            models.Index(fields=['-date_posted']),
        ]

    def __str__(self):
        return self.title

    @property
    def rating(self):
        """Вычисляет средний рейтинг на основе оценок пользователей"""
        ratings = self.ratings.all()
        if ratings.exists():
            return round(sum(r.value for r in ratings) / ratings.count(), 1)
        return None
    
    @property
    def user_rating(self, user):
        """Возвращает оценку пользователя"""
        return self.ratings.filter(user=user).first()
    
    @property
    def likes_count(self):
        return self.likes.count()

    def get_absolute_url(self):
        return reverse('blog-post', kwargs={'post_id': self.pk})

    def like(self, user):
        """Переключает лайк пользователя"""
        if user in self.likes.all():
            self.likes.remove(user)
            return False
        self.likes.add(user)
        return True

    def likes_count(self):
        """Возвращает количество лайков"""
        return self.likes.count()

    def get_types_display(self):
        """Возвращает строку с перечислением типов через запятую"""
        return ", ".join([t.name for t in self.types.all()])
    get_types_display.short_description = 'Типы'

    objects = PostQuerySet.as_manager()

class PostRating(models.Model):
    """Модель для хранения оценок пользователей с возможностью редактирования"""
    RATING_CHOICES = [
        (1, '1 - Ужасно'),
        (2, '2 - Очень плохо'),
        (3, '3 - Плохо'),
        (4, '4 - Ниже среднего'),
        (5, '5 - Средне'),
        (6, '6 - Выше среднего'),
        (7, '7 - Хорошо'),
        (8, '8 - Очень хорошо'),
        (9, '9 - Отлично'),
        (10, '10 - Превосходно'),
    ]

    post = models.ForeignKey(
        Post, 
        on_delete=models.CASCADE, 
        related_name='ratings',
        verbose_name='Пост'
    )
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )
    value = models.PositiveSmallIntegerField(
        choices=RATING_CHOICES,
        verbose_name='Оценка'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата оценки'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата изменения'
    )

    class Meta:
        verbose_name = 'Оценка поста'
        verbose_name_plural = 'Оценки постов'
        unique_together = ('post', 'user')
        ordering = ['-updated_at']

    def __str__(self):
        return f'{self.user.username} → {self.post.title}: {self.value}'

    def save(self, *args, **kwargs):
        """Обновляем дату изменения при сохранении"""
        if self.pk:  # Только при обновлении существующей записи
            self.updated_at = timezone.now()
        super().save(*args, **kwargs)


class Comment(models.Model):
    """Модель для комментариев к постам"""
    post = models.ForeignKey(
        Post, 
        on_delete=models.CASCADE, 
        related_name='comments',
        verbose_name='Пост'
    )
    author = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        verbose_name='Автор'
    )
    content = models.TextField(verbose_name='Содержание')
    date_posted = models.DateTimeField(
        default=timezone.now, 
        verbose_name='Дата публикации'
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='Активен'
    )

    class Meta:
        ordering = ['date_posted']
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return f'Комментарий {self.author.username} к "{self.post.title}"'


class Banner(models.Model):
    """Модель для баннеров на сайте"""
    title = models.CharField(
        max_length=100, 
        verbose_name='Заголовок', 
        blank=True, 
        null=True
    )
    image = models.ImageField(
        upload_to='banners/%Y/%m/%d/', 
        verbose_name='Изображение'
    )
    description = models.TextField(
        verbose_name='Описание', 
        blank=True, 
        null=True
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='Активный',
        help_text='Отображать ли баннер на сайте'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )

    class Meta:
        verbose_name = 'Баннер'
        verbose_name_plural = 'Баннеры'
        ordering = ['-created_at']

    def __str__(self):
        return self.title if self.title else f'Баннер #{self.id}'


# Настройки админ-панели
@admin.register(PostRating)
class PostRatingAdmin(admin.ModelAdmin):
    list_display = ('post', 'user', 'value', 'created_at', 'updated_at')
    list_filter = ('value', 'created_at', 'post__types')
    search_fields = ('post__title', 'user__username')
    list_editable = ('value',)
    readonly_fields = ('created_at', 'updated_at')
    raw_id_fields = ('post', 'user')

    fieldsets = (
        (None, {
            'fields': ('post', 'user', 'value')
        }),
        ('Даты', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )