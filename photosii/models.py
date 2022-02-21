from django.db import models
from django.shortcuts import reverse
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    id = models.AutoField(primary_key=True)
    email = models.EmailField(unique=True)
    username = models.CharField(blank=True, null=True, max_length=150)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email


class Photo(models.Model):
    statuses = (
        ('n', 'Подходящая'),
        ('b', 'Не подходящая'),
    )

    id = models.AutoField(primary_key=True)
    image = models.ImageField(upload_to='')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True, related_name='photos')
    description = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=1, choices=statuses, default='n')
    tag = models.ForeignKey('Tag', on_delete=models.CASCADE, related_name='photos', db_index=True, null=True,
                            blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_ai_tag = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.pk} | {self.image}'

    def get_absolute_url(self):
        return reverse('photosii:photo_view', kwargs={'id': self.id})

    def is_good(self):
        return self.status == 'n'

    class Meta:
        ordering = ('-created_at', )


class Tag(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64, default='default', unique=True)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        ordering = ('-name', )
