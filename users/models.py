from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='upload/default_pics/profile.jpg', upload_to='upload/profile_pics', max_length=255)
    show_in_staff = models.BooleanField(default=False, help_text='Показывать в списке сотрудников компании')
    position = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.user.username} Profile'