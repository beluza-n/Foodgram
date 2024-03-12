import django_filters

from .models import Recipe


class RecipeFilter(django_filters.FilterSet):
    is_favorited = django_filters.NumberFilter(
        field_name='is_favorited',
        method='filter_is_favorited')
    is_in_shopping_cart = django_filters.NumberFilter(
        field_name='is_in_shopping_cart',
        method='filter_is_in_shopping_cart')
    tags = django_filters.CharFilter(method='filter_tags')

    def filter_tags(self, qs, name, value):
        return qs.filter(tags__slug__in=self.request.GET.getlist('tags'))

    class Meta:
        model = Recipe
        fields = ('author',)

    def filter_is_favorited(self, queryset, name, value):
        if value is not None:
            return queryset.filter(is_favorited=value)
        return queryset

    def filter_is_in_shopping_cart(self, queryset, name, value):
        if value is not None:
            return queryset.filter(is_in_shopping_cart=value)
        return queryset
