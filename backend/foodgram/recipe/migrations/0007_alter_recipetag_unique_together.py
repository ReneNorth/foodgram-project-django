# Generated by Django 4.1.7 on 2023-06-27 19:05

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("tags", "0002_alter_tag_options"),
        ("recipe", "0006_alter_recipetag_tag"),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="recipetag",
            unique_together={("tag", "recipe")},
        ),
    ]