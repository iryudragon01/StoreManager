from django.contrib import admin
from django.contrib.auth import get_user_model
from stock.models import Worker

# Register your models here.
User = get_user_model()


class UserAdmin(admin.ModelAdmin):
    search_fields = ['email']

    class Mata:
        model = User


admin.site.register(User, UserAdmin)
admin.site.register(Worker)