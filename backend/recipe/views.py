from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import RetrieveAPIView, ListAPIView
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404

from .models import Recipe, RecipeIngredients, Ingredients, Favorites

from .serializers import RecipeSerializer, IngredientsSerializer, FavoritedRecipeSerializer
from django.contrib.auth import get_user_model

User = get_user_model()


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    pagination_class = PageNumberPagination 


    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class ListIngredientsAPIView(ListAPIView):
    serializer_class = IngredientsSerializer
    queryset = Ingredients.objects.all()

class RetrieveIngredientsAPIView(RetrieveAPIView):
    serializer_class = IngredientsSerializer
    queryset = Ingredients.objects.all()

class APIFavorites(APIView):
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

        serializer = FavoritedRecipeSerializer(favorited_recipe)
        return Response(serializer.data)

    def delete(self, request, pk):
        user = request.user
        favorited_recipe = get_object_or_404(Recipe, pk=pk)
        try:
            Favorites.objects.get(user=user, recipe=favorited_recipe).delete()
        except:
            return Response({'detail': 'Recipe is not favorited'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_204_NO_CONTENT)
