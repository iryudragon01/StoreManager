from django.db import models
from django.contrib.auth.models import User as UserDjango


# Create your models here.
class User(models.Model):
    objects: models.Manager
    user = models.OneToOneField(UserDjango,on_delete=models.CASCADE)
    own = models.PositiveIntegerField(default=2)    # number of worker
    key = models.PositiveIntegerField(default=0)

    def __unicode__(self):
        return self.username


class UserExtend(models.Model):
    objects: models.Manager
    owner = models.ForeignKey(User,on_delete=models.CASCADE)
    username = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    date_log = models.DateTimeField(auto_now=True)
    access_level = models.PositiveIntegerField()  # 1-99


class Item(models.Model):
    objects: models.manager
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    price = models.PositiveIntegerField()
    type = models.PositiveSmallIntegerField(choices=[(1, 'Non Stock'), (2, 'Air pay'), (3, 'Stock')])
    is_active = models.PositiveSmallIntegerField(choices=[(0, 'inactive'), (1, 'active')])
    user_access = models.PositiveSmallIntegerField()

    def __unicode__(self):
        return self.name


class Stock(models.Model):
    objects: models.manager
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    volume = models.PositiveIntegerField()
    create_user = models.CharField(max_length=200)
    create_time = models.DateTimeField(auto_now=True)
    edit_user = models.CharField(max_length=200)
    edit_time = models.DateTimeField(auto_now=True)


class Sale(models.Model):
    objects: models.manager
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    volume = models.PositiveIntegerField()
    create_user = models.CharField(max_length=200)
    create_time = models.DateTimeField(auto_now=True)
    edit_user = models.CharField(max_length=200)
    edit_time = models.DateTimeField(auto_now=True)
