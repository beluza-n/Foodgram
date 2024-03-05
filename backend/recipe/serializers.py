import base64

from django.core.files.base import ContentFile
from rest_framework import serializers

from .models import Recipe, RecipeIngredients, Ingredients, Tags, TagRecipe
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
    ingredients = RecipeIngredientsSerializer(required=False, many=True)
    tags = serializers.PrimaryKeyRelatedField(many=True, queryset=Tags.objects.all(), read_only=False)
    image = Base64ImageField(required=False, allow_null=True)
    
    
    class Meta:
        model = Recipe
        fields = ('name', 'text', 'cooking_time', 'ingredients', 'tags', 'image')

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
        
    def to_representation(self, data):
        return RecipeResponseSerializer(context=self.context).to_representation(data)
        

class RecipeResponseSerializer(serializers.ModelSerializer):
    tags = TagsResponseSerializer(required=False, many=True)
    # image = Base64ImageField(required=False, allow_null=True)
    author = CustomUserSerializer()
    ingredients = RecipeIngredientsResponseSerializer(required=False, many=True)
    
    class Meta:
        model = Recipe
        fields = ('id', 'author', 'ingredients', 'tags', 'name', 'text', 'cooking_time')
        read_only_fields = ('author',)



