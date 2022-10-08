from django.contrib import admin
from .models import Adverts


class AdvertsAdmin(admin.ModelAdmin):
    list_display = ('Ad_Title', 'price', 'sq_ft')

admin.site.register(Adverts, AdvertsAdmin)