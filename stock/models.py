from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, is_active=True, is_staff=False, is_admin=False):
        if not email:
            raise ValueError('user must have an email address ')
        if not password:
            raise ValueError('user must have a password')
        user_obj = self.model(
            email=self.normalize_email(email)
        )
        user_obj.active = is_active
        user_obj.staff = is_staff
        user_obj.admin = is_admin
        user_obj.set_password(password)     # change user password
        user_obj.save(self._db)
        return user_obj

    def create_staffuser(self, email, password=None):
        user = self.create_user(
            email=email,
            password=password,
            is_staff=True
        )
        return user

    def create_superuser(self, email, password=None):
        user = self.create_user(
            email=email,
            password=password,
            is_staff=True,
            is_admin=True
        )
        return user


class User(AbstractBaseUser):
    email = models.EmailField(max_length=255, unique=True)
    full_name = models.CharField(max_length=255, blank=True, null=True)
    active = models.BooleanField(default=True)   # can login
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now=True)
    confirm = models.BooleanField(default=False)
    confirm_date = models.DateTimeField(null=True)

    USERNAME_FIELD = 'email'
    # USERNAME_FIELD and password are required by default
    REQUIRED_FIELDS = []  # ['full_name']   # python manage.py createsuperuser
    objects = UserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_active(self):
        return self.active

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin




    # objects: models.Manager
    # user = models.OneToOneField(UserDjango,on_delete=models.CASCADE)
    # own = models.PositiveIntegerField(default=2)    # number of worker
    # key = models.PositiveIntegerField(default=0)
    #
    # def __unicode__(self):
    #     return self.username


class Worker(models.Model):
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
