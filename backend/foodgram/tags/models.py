from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name='Тэг')
    color = models.CharField(max_length=7, unique=True, verbose_name='Цвет',
                             help_text='Введите цвет в HEX формате')
    slug = models.SlugField(max_length=50, unique=True, verbose_name='Cсылка')

    class Meta:
        ordering = ['-id']

    def __str__(self) -> str:
        """Return the name field of the model."""
        return self.name
