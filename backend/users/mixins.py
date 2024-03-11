from rest_framework import serializers

from .models import UserFollowing


class IsSubscribedSerializerMixin(serializers.Serializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        fields = ('is_subscribed', )

    def get_is_subscribed(self, obj):
        current_user = self.context.get('request').user
        is_subscribed = (
            UserFollowing.objects.
            filter(user=current_user.id, following_user=obj.id).exists())
        return is_subscribed
