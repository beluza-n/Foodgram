import base64
from rest_framework import serializers
from rest_framework.response import Response
from djoser.serializers import UserCreateSerializer, UserSerializer
from .models import UserFollowing
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from .mixins import IsSubscribedSerializerMixin

from recipe.models import Recipe
# from recipe.serializers import ShortRecipeSerializer


User = get_user_model()


class CustomUserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        fields = ('email', 'id', 'username', 'first_name', 'last_name', 'password', )
        extra_kwargs = {'first_name': {'required': True, 'allow_blank': False},
                        'last_name': {'required': True,'allow_blank': False},
                        'email': {'required': True,'allow_blank': False} }




class CustomUserSerializer(UserSerializer, IsSubscribedSerializerMixin):
# class CustomUserSerializer(UserSerializer):
    # is_subscribed = serializers.SerializerMethodField()

    class Meta(UserSerializer.Meta):
        fields = ('email', 'id', 'username', 'first_name', 'last_name', 'is_subscribed')

    # def get_is_subscribed(self, obj):
    #     current_user = self.context['request'].user
    #     is_subscribed = UserFollowing.objects.filter(user=current_user.id, following_user=obj.id).exists()
    #     return is_subscribed

class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]

            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        return super().to_internal_value(data)

class ShortRecipeSerializer_2(serializers.ModelSerializer):
    image = Base64ImageField(required=False, allow_null=True)
    
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')

class CustomUserWithRecipeSerializer(UserSerializer, IsSubscribedSerializerMixin):
    recipes = serializers.SerializerMethodField()
    # recipes_count = serializers.SerializerMethodField()



    class Meta(UserSerializer.Meta):
        fields = ('email', 'id', 'username', 'first_name', 'last_name', 'is_subscribed', 'recipes')

    def get_recipes(self, obj):
        request = self.context['request']
        recipes_limit = int(request.query_params['recipes_limit'])
        queryset = Recipe.objects.filter(author_id=obj.id).order_by('-created_at')[:recipes_limit]
        # serializer = ShortRecipeSerializer(queryset, many=True)
        serializer = ShortRecipeSerializer_2(queryset, many=True, read_only=True)
        return serializer.data
        
       



class FollowingSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserFollowing
        fields = ("id", "user", "following_user", "created")