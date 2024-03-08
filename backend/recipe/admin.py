from django.contrib import admin
from .models import Recipe, Ingredients, Tags, RecipeIngredients

class TagsInline(admin.TabularInline):
    model = Recipe.tags.through
    extra = 0

class RecipeIngredientsInline(admin.TabularInline):
    model = RecipeIngredients
    extra = 0
    fields = ('name', 'amount', 'units')
    readonly_fields = ('units',)

    def units(self, instance):
        return instance.name.measurement_unit
        

class RecipeAdmin(admin.ModelAdmin):
    filter_horizontal = ('tags',)
    inlines = (
        RecipeIngredientsInline,
        TagsInline
    )
    list_display = (
        'name',
        'author',
    )
    search_fields = ('author', 'name') 
    list_filter = ('author', 'name', 'tags')


class IngredientsAdmin(admin.ModelAdmin):
    search_fields = ('name',) 


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingredients, IngredientsAdmin)
admin.site.register(Tags)
admin.site.register(RecipeIngredients)