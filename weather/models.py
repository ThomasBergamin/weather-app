from django.db import models
from django.urls import reverse

# Create your models here.


class City(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('home')

    class Meta:
        verbose_name_plural = 'cities'
