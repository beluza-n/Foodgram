from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from .models import UserFollowing
from .serializers import CustomUserSerializer, CustomUserWithRecipeSerializer

User = get_user_model()

# from serializers import UserFollowingSerializer


# class UserFollowingViewSet(viewsets.ModelViewSet):
#     # permission_classes = (IsAuthenticatedOrReadOnly,)
#     serializer_class = UserFollowingSerializer
#     queryset = models.UserFollowing.objects.all()


class SubscribeAPIView(APIView):
    """
    Subscribe or unsubscribe.
    """
    def post(self, request, pk):
        user = request.user
        follow = get_object_or_404(User, pk=pk)
        if user.id == pk:
            return Response({'detail': 'Cannot subscribe to youself'}, status.HTTP_400_BAD_REQUEST)
        try:
            UserFollowing.objects.create(user=user, following_user=follow)
        except:
            return Response({'detail': 'Already subscribed'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = CustomUserWithRecipeSerializer(follow, context={'request': request})
        return Response(serializer.data)

    def delete(self, request, pk):
        user = request.user
        follow = get_object_or_404(User, pk=pk)
        try:
            UserFollowing.objects.get(user=user, following_user=follow).delete()
        except:
            return Response({'detail': 'You are not subscribed'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_204_NO_CONTENT)


# class SubscriptionsAPIView(APIView):
#     def get(self, request):
#         current_user = request.user
#         subscribed_to = current_user.following.all().values_list('following_user_id')
#         queryset = User.objects.filter(id__in = subscribed_to)
#         serializer = CustomUserSerializer(queryset, many=True, context={'request': request})
#         return Response(serializer.data)
        
class SubscriptionsAPIView(ListAPIView):
    """
    Show all my subscriptions.
    """
    serializer_class = CustomUserWithRecipeSerializer

    def get_queryset(self):
        current_user = self.request.user
        subscribed_to = current_user.following.all().values_list('following_user_id')
        queryset = User.objects.filter(id__in = subscribed_to)
        return queryset
