# Generated by Django 2.2.7 on 2019-12-06 11:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0016_statement'),
    ]

    operations = [
        migrations.AddField(
            model_name='sale',
            name='sale_price',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
