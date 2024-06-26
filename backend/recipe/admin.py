from django.contrib import admin
from .models import Recipe, Ingredients, Tags, RecipeIngredients
from django.db.models import Count


class TagsInline(admin.TabularInline):
    model = Recipe.tags.through
    extra = 0
    min_num = 1

    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj=None, **kwargs)
        formset.validate_min = True
        return formset


class RecipeIngredientsInline(admin.TabularInline):
    model = Recipe.recipe_ingredients.through
    extra = 0
    min_num = 1
    fields = ('name', 'amount', 'units')
    readonly_fields = ('units',)

    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj=None, **kwargs)
        formset.validate_min = True
        return formset

    def units(self, instance):
        return instance.name.measurement_unit


class RecipeAdmin(admin.ModelAdmin):
    filter_horizontal = ('tags',)
    inlines = (
        RecipeIngredientsInline,
        TagsInline
    )
    list_filter = ('author', 'name', 'tags')
    list_display = (
        'name',
        'author',
        'is_favorited_count'
    )
    search_fields = ('author', 'name')
    readonly_fields = ('is_favorited_count',)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(is_favorited_count=Count('favorites'))
        return queryset

    def is_favorited_count(self, obj):
        return obj.is_favorited_count


class IngredientsAdmin(admin.ModelAdmin):
    search_fields = ('name',)


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingredients, IngredientsAdmin)
admin.site.register(Tags)
admin.site.register(RecipeIngredients)
