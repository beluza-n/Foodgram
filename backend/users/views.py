from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from .models import UserFollowing
from .serializers import CustomUserWithRecipeSerializer

User = get_user_model()


class SubscribeAPIView(APIView):
    """
    Subscribe or unsubscribe.
    """
    permission_classes = (IsAuthenticated, )

    def post(self, request, pk):
        self.check_permissions(request)
        user = request.user
        follow = get_object_or_404(User, pk=pk)
        if user.id == pk:
            return Response(
                {'detail': 'Cannot subscribe to youself'},
                status.HTTP_400_BAD_REQUEST)
        if UserFollowing.objects.filter(user=user,
                                        following_user=follow).exists():
            return Response(
                {'detail': 'Already subscribed'},
                status=status.HTTP_400_BAD_REQUEST)
        else:
            UserFollowing.objects.create(user=user, following_user=follow)

        serializer = CustomUserWithRecipeSerializer(
            follow,
            context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, pk):
        self.check_permissions(request)
        user = request.user
        follow = get_object_or_404(User, pk=pk)
        try:
            UserFollowing.objects.get(user=user,
                                      following_user=follow).delete()
        except UserFollowing.DoesNotExist:
            return Response(
                {'detail': 'You are not subscribed'},
                status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_204_NO_CONTENT)


class SubscriptionsAPIView(ListAPIView):
    """
    Show all my subscriptions.
    """
    serializer_class = CustomUserWithRecipeSerializer
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        current_user = self.request.user
        subscribed_to = (current_user.following.all().
                         values_list('following_user_id'))
        queryset = User.objects.filter(id__in=subscribed_to)
        return queryset
