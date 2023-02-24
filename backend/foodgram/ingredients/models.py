from django.db import models


class Ingredient(models.Model):
    name = models.CharField(unique=True, max_length=40)
    measurement_unit = models.CharField(max_length=20)

    def __str__(self):
        return f'{self.name} в {self.measurement_unit}'
