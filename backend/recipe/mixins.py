# from rest_framework import serializers

# from .models import Favorites, ShoppingCart


# class IsFavoritedSerializerMixin(serializers.Serializer):
#     is_favorited = serializers.SerializerMethodField()

#     class Meta:
#         fields = ('is_subscribed', )

#     def get_is_favorited(self, obj):
#         current_user = self.context.get('request').user
#         is_subscribed = Favorites.objects.filter(user=current_user.id, recipe=obj.id).exists()
#         return is_subscribed
    
# class IsInShoppingCartSerializerMixin(serializers.Serializer):
#     is_in_shopping_cart = serializers.SerializerMethodField()

#     class Meta:
#         fields = ('is_in_shopping_cart', )

#     def get_is_in_shopping_cart(self, obj):
#         current_user = self.context.get('request').user
#         is_in_shopping_cart = ShoppingCart.objects.filter(user=current_user.id, recipe=obj.id).exists()
#         return is_in_shopping_cart