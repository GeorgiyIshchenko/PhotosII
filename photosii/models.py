from django.db import models
from django.shortcuts import reverse


class Photo(models.Model):
    statuses = (
        ('n', 'Подходящая'),
        ('b', 'Не подходящая'),
    )

    id = models.AutoField(primary_key=True)
    image = models.ImageField(upload_to='')
    description = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=1, choices=statuses, default='n')
    tag = models.ForeignKey('Tag', on_delete=models.CASCADE, related_name='photos', db_index=True, null=True,
                            blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.image}'

    def get_absolute_url(self):
        return reverse('photosii:photo_view', kwargs={'id': self.id})

    def is_good(self):
        return self.status == 'n'


class Tag(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64, default='default', unique=True)

    def __str__(self):
        return f'{self.name}'
