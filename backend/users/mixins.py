from rest_framework import mixins, viewsets, serializers
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import SearchFilter

from .models import UserFollowing

# from .permissions import IsAdminUserOrReadOnly

class IsSubscribedSerializerMixin(serializers.Serializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        fields = ('is_subscribed', )

    def get_is_subscribed(self, obj):
        current_user = self.context.get('request').user
        is_subscribed = UserFollowing.objects.filter(user=current_user.id, following_user=obj.id).exists()
        return is_subscribed


# class CreateDestroyViewSet(
#     mixins.CreateModelMixin,
#     mixins.DestroyModelMixin,
#     viewsets.GenericViewSet
# ):
#     pass


# class NameViewSetMixin(CreateDestroyViewSet):
#     permission_classes = [IsAuthenticatedOrReadOnly, IsAdminUserOrReadOnly]
#     pagination_class = PageNumberPagination
#     filter_backends = (SearchFilter,)
#     lookup_field = 'slug'
#     search_fields = ('name',)