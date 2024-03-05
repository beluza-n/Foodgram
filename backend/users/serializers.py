from rest_framework import serializers
from djoser.serializers import UserCreateSerializer, UserSerializer
from .models import UserFollowing
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from .mixins import IsSubscribedSerializerMixin

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




class FollowingSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserFollowing
        fields = ("id", "user", "following_user", "created")