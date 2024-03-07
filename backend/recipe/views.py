from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import RetrieveAPIView, ListAPIView
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework import filters

from rest_framework.permissions import IsAuthenticated, AllowAny

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.db.models import Sum, F, Count, Q, Case, When, BooleanField

from .models import Recipe, RecipeIngredients, Ingredients, Favorites, ShoppingCart, Tags
from .pagination import CustomPageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend

from .filters import RecipeFilter
from .permissions import ReadOnly, IsAuthorOrReadOnly


from .serializers import (
    RecipeSerializer,
    IngredientsSerializer,
    ShortRecipeSerializer,
    TagsSerializer,
    DownloadShoppingCartSerializer)

from django.contrib.auth import get_user_model

User = get_user_model()


class RecipeViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'patch','delete', 'head', 'option']
    serializer_class = RecipeSerializer
    pagination_class = CustomPageNumberPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return (ReadOnly(),)
        if self.action == 'create':
            return (IsAuthenticated(),)
        if self.action in ['update', 'partial_update', 'destroy']:
            return (IsAuthorOrReadOnly(),)
        return (super().get_permissions() )


    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_queryset(self):
        user = self.request.user
        user_id = user.id if not user.is_anonymous else None
        queryset = Recipe.objects.all().annotate(
            total_favorite=Count(
                "favorites",
                filter=Q(favorites__user_id=user_id)
            ),
            is_favorited=Case(
                When(total_favorite__gte=1, then=True),
                default=False,
                output_field=BooleanField()
            )
        )
        queryset = queryset.annotate(
            total_shopping_cart=Count(
                "shopping_cart",
                filter=Q(shopping_cart__user_id=user_id)
            ),
            is_in_shopping_cart=Case(
                When(total_shopping_cart__gte=1, then=True),
                default=False,
                output_field=BooleanField()
            )
        )
        return queryset


class ListIngredientsAPIView(ListAPIView):
    serializer_class = IngredientsSerializer
    queryset = Ingredients.objects.all()
    permission_classes = (AllowAny,)
    pagination_class = None
    filter_backends = (filters.SearchFilter,)
    search_fields = ('^name',)

class RetrieveIngredientsAPIView(RetrieveAPIView):
    serializer_class = IngredientsSerializer
    queryset = Ingredients.objects.all()
    permission_classes = (AllowAny,)


class ListTagsAPIView(ListAPIView):
    serializer_class = TagsSerializer
    queryset = Tags.objects.all()
    pagination_class = None
    permission_classes = (AllowAny,)

class RetrieveTagsAPIView(RetrieveAPIView):
    serializer_class = TagsSerializer
    queryset = Tags.objects.all()
    permission_classes = (AllowAny,)

class FavoritesAPIView(APIView):
    """
    Add or remove recipe from favorites.
    """
    permission_classes = (IsAuthenticated, )

    def post(self, request, pk):
        self.check_permissions(request)
        user = request.user
        favorited_recipe = get_object_or_404(Recipe, pk=pk)
        try:
            Favorites.objects.create(user=user, recipe=favorited_recipe)
        except:
            return Response({'detail': 'Already favorited'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = ShortRecipeSerializer(favorited_recipe)
        return Response(serializer.data)

    def delete(self, request, pk):
        self.check_permissions(request)
        user = request.user
        favorited_recipe = get_object_or_404(Recipe, pk=pk)
        try:
            Favorites.objects.get(user=user, recipe=favorited_recipe).delete()
        except:
            return Response({'detail': 'Recipe is not favorited'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_204_NO_CONTENT)


class ShoppingCartAPIview(APIView):
    """
    Add or remove recipe from shopping cart.
    """
    permission_classes = (IsAuthenticated, )

    def post(self, request, pk):
        self.check_permissions(request)
        user = request.user
        recipe = get_object_or_404(Recipe, pk=pk)
        try:
            ShoppingCart.objects.create(user=user, recipe=recipe)
        except:
            return Response({'detail': 'Already in shopping cart'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = ShortRecipeSerializer(recipe)
        return Response(serializer.data)

    def delete(self, request, pk):
        self.check_permissions(request)
        user = request.user
        recipe = get_object_or_404(Recipe, pk=pk)
        try:
            ShoppingCart.objects.get(user=user, recipe=recipe).delete()
        except:
            return Response({'detail': 'Recipe is not in shopping cart'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_204_NO_CONTENT)
    


class DownloadShoppingCartAPIview(APIView):
    """
    Download file with sum of ingredients.
    """
    permission_classes = (IsAuthenticated, )

    def get(self, request, format=None):
        self.check_permissions(request)
        recipe_ingredients = RecipeIngredients.objects.filter(
            recipe__shopping_cart__user=request.user)
        queryset = (recipe_ingredients.values("name_id__name", "name_id__measurement_unit").annotate(sum=Sum(F("amount"))).filter(sum__gt=0).order_by("-sum"))
        serializer = DownloadShoppingCartSerializer(queryset, many=True)
        ingredients_list = []
        ingredients_list = [data.get("ingredient_amount") for data in serializer.data]
        header = 'Ваш список покупок\n'
        delimiter = "\n"
        result_string = header + delimiter.join(ingredients_list)
        filename = 'ShoppingCart.txt'
        response = HttpResponse(result_string, content_type='text/plain; charset=UTF-8')
        response['Content-Disposition'] = ('attachment; filename={0}'.format(filename))
        return response