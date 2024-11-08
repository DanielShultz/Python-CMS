from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='upload/default_pics/profile.jpg', upload_to='upload/profile_pics', max_length=255)

    def __str__(self):
        return f'{self.user.username} Profile'