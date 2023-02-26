from django.db import models
# from recipe.models import Recipe


class Tag(models.Model):
    name = models.CharField(max_length=50, verbose_name='Тэг')
    color = models.CharField(max_length=50, verbose_name='Цвет') # к переделке
    slug = models.SlugField(max_length=50, verbose_name='Cсылка')


