import django_filters
from .models import Recipe


class RecipeFilter(django_filters.FilterSet):
    is_favorited = django_filters.NumberFilter(field_name='is_favorited', method='filter_is_favorited')
    is_in_shopping_cart = django_filters.NumberFilter(field_name='is_in_shopping_cart', method='filter_is_in_shopping_cart')
    tags = django_filters.CharFilter(field_name='tags__slug')

    class Meta:
        model = Recipe
        fields = (
            'author',
            )
        
    def filter_is_favorited(self, queryset, name, value):
        if value is not None:
            if value == 1:
                return queryset.filter(is_favorited=True)
            else:
                return queryset.filter(is_favorited=False)
        else:
            return queryset
        
    def filter_is_in_shopping_cart(self, queryset, name, value):
        if value is not None:
            if value == 1:
                return queryset.filter(is_in_shopping_cart=True)
            else:
                return queryset.filter(is_in_shopping_cart=False)
        else:
            return queryset