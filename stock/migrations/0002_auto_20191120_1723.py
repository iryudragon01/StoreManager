# Generated by Django 2.2.7 on 2019-11-20 10:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='worker',
            name='access_level',
            field=models.PositiveIntegerField(choices=[(1, 'admin'), (10, 'superuser'), (99, 'worker')], default=99),
        ),
    ]