from django.contrib import admin

from .models import Recipe, Tags

admin.site.register(Recipe)
admin.site.register(Tags)