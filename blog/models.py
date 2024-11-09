from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Post(models.Model):
    title = models.CharField(max_length=100)
    type = models.ForeignKey('Type', on_delete=models.CASCADE)
    content = models.TextField()
    rating = models.IntegerField(blank=True, null=True)
    price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    date_posted = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='upload/post_pics', blank=True, null=True)

    class Meta:
        ordering = ['title']

    def get_absolute_url(self):
        return f'/post/{self.id}'
    
    def next_post(self):
        return Post.objects.filter(date_posted__gt=self.date_posted, type=self.type).order_by('date_posted').first()
    
    def prev_post(self):
        return Post.objects.filter(date_posted__lt=self.date_posted, type=self.type).order_by('-date_posted').first()

    def __str__(self):
        return self.title
    
class Type(models.Model):
    name = models.CharField(max_length=100)
    plural = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.plural:
            self.plural = self.name
        super().save(*args, **kwargs)
