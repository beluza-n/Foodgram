from rest_framework import serializers

from .models import Favorites


class IsFavoritedSerializerMixin(serializers.Serializer):
    is_favorited = serializers.SerializerMethodField()

    class Meta:
        fields = ('is_subscribed', )

    def get_is_favorited(self, obj):
        current_user = self.context.get('request').user
        is_subscribed = Favorites.objects.filter(user=current_user.id, recipe=obj.id).exists()
        return is_subscribed