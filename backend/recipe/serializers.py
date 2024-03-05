import base64

from django.core.files.base import ContentFile
from rest_framework import serializers

from .models import Recipe, RecipeIngredients, Ingredients, Tags, TagRecipe
from .mixins import IsFavoritedSerializerMixin
from users.serializers import CustomUserSerializer


class IngredientsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredients
        fields = ('id', 'name', 'measurement_unit')


class RecipeIngredientsSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(many=False, queryset = Ingredients.objects.all())

    class Meta:
        model = RecipeIngredients
        fields = ('id', 'amount')

class RecipeIngredientsResponseSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='name.id')
    name = serializers.CharField(source='name.name')
    measurement_unit = serializers.CharField(source='name.measurement_unit')

    class Meta:
        model = RecipeIngredients
        fields = ('id', 'name', 'measurement_unit','amount')

class TagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tags
        fields = ('id',)

class TagsResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tags
        fields = ('id', 'name', 'color', 'slug')


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]

            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        return super().to_internal_value(data)


class RecipeSerializer(serializers.ModelSerializer):
    ingredients = RecipeIngredientsSerializer(required=True, many=True)
    tags = serializers.PrimaryKeyRelatedField(required=True, many=True, queryset=Tags.objects.all(), read_only=False)
    image = Base64ImageField(required=True, allow_null=True)
    
    
    class Meta:
        model = Recipe
        fields = ('name', 'text', 'cooking_time', 'ingredients', 'tags', 'image')

    def __init__(self, *args, **kwargs):
        kwargs['partial'] = False
        super(RecipeSerializer, self).__init__(*args, **kwargs)

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)
        for ingredient in ingredients:
            RecipeIngredients.objects.create(
                recipe=recipe, name=ingredient['id'], amount=ingredient['amount']
                )
        for tag in tags:
            TagRecipe.objects.create(tag=tag, recipe=recipe)
        return recipe
    
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.text = validated_data.get('text', instance.text)
        instance.cooking_time = validated_data.get(
            'cooking_time', instance.cooking_time
            )
        instance.image = validated_data.get('image', instance.image)
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        RecipeIngredients.objects.filter(recipe=instance).delete()
        TagRecipe.objects.filter(recipe=instance).delete()
        for ingredient in ingredients:
            RecipeIngredients.objects.create(
                recipe=instance, name=ingredient['id'], amount=ingredient['amount']
                )
        lst_tags = []
        for tag in tags:
            lst_tags.append(tag)
        instance.tags.set(lst_tags)


        instance.save()
        return instance
        
    def to_representation(self, data):
        return RecipeResponseSerializer(context=self.context).to_representation(data)
        

class RecipeResponseSerializer(serializers.ModelSerializer, IsFavoritedSerializerMixin):
    tags = TagsResponseSerializer(required=False, many=True)
    image = Base64ImageField(required=False, allow_null=True)
    author = CustomUserSerializer()
    ingredients = RecipeIngredientsResponseSerializer(many=True)
    
    class Meta:
        model = Recipe
        fields = ('id', 'author', 'ingredients', 'tags', 'name', 'image', 'text', 'cooking_time', 'is_favorited')
        read_only_fields = ('author',)


class FavoritedRecipeSerializer(serializers.ModelSerializer):
    image = Base64ImageField(required=False, allow_null=True)
    
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')

