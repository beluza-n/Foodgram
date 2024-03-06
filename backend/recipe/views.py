from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import RetrieveAPIView, ListAPIView
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.db.models import Sum, F

from .models import Recipe, RecipeIngredients, Ingredients, Favorites, ShoppingCart, Tags
from .pagination import CustomPageNumberPagination

from .serializers import (
    RecipeSerializer,
    IngredientsSerializer,
    ShortRecipeSerializer,
    TagsSerializer,
    DownloadShoppingCartSerializer)

from django.contrib.auth import get_user_model

User = get_user_model()


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    pagination_class = CustomPageNumberPagination 


    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class ListIngredientsAPIView(ListAPIView):
    serializer_class = IngredientsSerializer
    queryset = Ingredients.objects.all()
    pagination_class = None

class RetrieveIngredientsAPIView(RetrieveAPIView):
    serializer_class = IngredientsSerializer
    queryset = Ingredients.objects.all()


class ListTagsAPIView(ListAPIView):
    serializer_class = TagsSerializer
    queryset = Tags.objects.all()
    pagination_class = None

class RetrieveTagsAPIView(RetrieveAPIView):
    serializer_class = TagsSerializer
    queryset = Tags.objects.all()

class FavoritesAPIView(APIView):
    """
    Add or remove recipe from favorites.
    """
    def post(self, request, pk):
        user = request.user
        favorited_recipe = get_object_or_404(Recipe, pk=pk)
        try:
            Favorites.objects.create(user=user, recipe=favorited_recipe)
        except:
            return Response({'detail': 'Already favorited'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = ShortRecipeSerializer(favorited_recipe)
        return Response(serializer.data)

    def delete(self, request, pk):
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
    def post(self, request, pk):
        user = request.user
        recipe = get_object_or_404(Recipe, pk=pk)
        try:
            ShoppingCart.objects.create(user=user, recipe=recipe)
        except:
            return Response({'detail': 'Already in shopping cart'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = ShortRecipeSerializer(recipe)
        return Response(serializer.data)

    def delete(self, request, pk):
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
    def get(self, request, format=None):
        recipe_ingredients = RecipeIngredients.objects.filter(
            recipe__shopping_cart__user=request.user)
        queryset = (recipe_ingredients.values("name_id__name", "name_id__measurement_unit").annotate(sum=Sum(F("amount"))).filter(sum__gt=0).order_by("-sum"))
        serializer = DownloadShoppingCartSerializer(queryset, many=True)
        ingredients_list = []
        ingredients_list = [data.get("ingredient_amount") for data in serializer.data]
        header = 'Ваш список покупок\n'
        delimiter = "\n"
        result_string = header + delimiter.join(ingredients_list)
        print(result_string)

            
                
        filename = 'ShoppingCart.txt'
        # response = HttpResponse(ingredients_list, content_type='text/plain; charset=UTF-8')
        response = HttpResponse(result_string, content_type='text/plain; charset=UTF-8')
        response['Content-Disposition'] = ('attachment; filename={0}'.format(filename))
        # print(ingredients_list)
        return response
        
        # return Response(ingredients_list)
