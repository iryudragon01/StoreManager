# Generated by Django 2.2.7 on 2019-11-23 12:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0004_auto_20191121_2020'),
    ]

    operations = [
        migrations.AlterField(
            model_name='worker',
            name='username',
            field=models.SlugField(max_length=200, unique=True),
        ),
    ]
