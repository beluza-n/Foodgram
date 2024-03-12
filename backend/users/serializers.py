from rest_framework import serializers
from djoser.serializers import UserCreateSerializer, UserSerializer
from django.contrib.auth import get_user_model

from .models import UserFollowing
from .mixins import IsSubscribedSerializerMixin
from recipe.models import Recipe

from . import constants as const


User = get_user_model()


class CustomUserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        fields = (
            'email', 'id',
            'username',
            'first_name',
            'last_name',
            'password', )
        extra_kwargs = {
            'first_name': {'required': True,
                           'allow_blank': False,
                           'max_length': const.MAX_LENGTH_FIRST_NAME},
            'last_name': {'required': True,
                          'allow_blank': False,
                          'max_length': const.MAX_LENGTH_LAST_NAME},
            'email': {'required': True,
                      'allow_blank': False,
                      'max_length': const.MAX_LENGTH_EMAIL},
            'username': {'max_length': const.MAX_LENGTH_USERNAME},
            'password': {'max_length': const.MAX_LENGTH_PASSWORD}}


class CustomUserSerializer(UserSerializer, IsSubscribedSerializerMixin):

    class Meta(UserSerializer.Meta):
        fields = (
            'email', 'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed')


class ShortRecipeSerializer(serializers.ModelSerializer):
    image = serializers.CharField(source='image.url')

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class CustomUserWithRecipeSerializer(UserSerializer,
                                     IsSubscribedSerializerMixin):
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta(UserSerializer.Meta):
        fields = (
            'email', 'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count')

    def get_recipes(self, obj):
        request = self.context['request']
        recipes_limit = request.query_params.get('recipes_limit', None)
        if recipes_limit:
            queryset = (Recipe.objects.filter(author_id=obj.id).
                        order_by('-created_at')[:int(recipes_limit)])
        else:
            queryset = (Recipe.objects.filter(author_id=obj.id).
                        order_by('-created_at'))
        serializer = ShortRecipeSerializer(queryset,
                                           many=True,
                                           read_only=True)
        return serializer.data

    def get_recipes_count(self, obj):
        return Recipe.objects.filter(author_id=obj.id).count()


class FollowingSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserFollowing
        fields = ("id", "user", "following_user", "created")
