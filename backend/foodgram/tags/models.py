from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name='Тэг')
    color = models.CharField(max_length=50, unique=True, verbose_name='Цвет')
    slug = models.SlugField(max_length=50, unique=True, verbose_name='Cсылка')

    def __str__(self) -> str:
        """Return the name field of the model."""
        return self.name
