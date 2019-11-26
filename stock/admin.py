from django.contrib import admin
from django.contrib.auth import get_user_model
from stock.models import Worker,Item,Sale

# Register your models here.
User = get_user_model()


class UserAdmin(admin.ModelAdmin):
    search_fields = ['email']

    class Mata:
        model = User

class SaleAdmin(admin.ModelAdmin):
    search_fields=['item__name']
    class Meta:
        model = Sale

admin.site.register(User, UserAdmin)
admin.site.register(Worker)
admin.site.register(Item)
admin.site.register(Sale,SaleAdmin)