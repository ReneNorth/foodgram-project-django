from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name='Tag')
    color = models.CharField(max_length=7, unique=True, verbose_name='Color',
                             help_text='Color in HEX format')
    slug = models.SlugField(max_length=50, unique=True, verbose_name='Slug')

    class Meta:
        ordering = ['-id']

    def __str__(self) -> str:
        """Return the name field of the model."""
        return self.name
