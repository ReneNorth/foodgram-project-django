# Generated by Django 4.1.7 on 2023-07-15 19:48

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("recipe", "0011_alter_recipetag_unique_together_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="recipe",
            name="pub_date",
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
