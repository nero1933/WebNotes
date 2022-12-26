from django.contrib.auth.models import User, AbstractUser, UserManager
from django.db import models
from django.urls import reverse


# Create your models here.
class Note(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)
    content = models.TextField()
    icon = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    time_created = models.DateTimeField(auto_now_add=True)
    time_updated = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    folder = models.ForeignKey('Folder', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('show_note', kwargs={'username': self.user.username, 'note_slug': self.slug})


class Folder(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    time_created = models.DateTimeField(auto_now_add=True)
    time_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('show_folder', kwargs={'username': self.user.username, 'folder_slug': self.slug})


# CustomUser


# class CustomUserManager(UserManager):
#     def get(self, *args, **kwargs):
#         return super().select_related().get(*args, **kwargs)
#
#
# class CustomUser(AbstractUser):
#     objects = CustomUserManager()
