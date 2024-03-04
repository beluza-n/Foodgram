import base64

from django.core.files.base import ContentFile
from rest_framework import serializers

from .models import Recipe, RecipeIngredients, Ingredients, Tags
from users.serializers import CustomUserSerializer


class IngredientsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredients
        fields = ('id', 'name', 'measurement_unit')



class MeasurementUnitField(serializers.RelatedField):
    # class Meta:
    #     model = RecipeIngredients
    #     fields = ['measurement_unit',]
    #     read_only_fields = ['measurement_unit']

    def to_representation(self, value):
        return value.name_id.measurement_unit


class RecipeIngredientsSerializer(serializers.ModelSerializer):
    
    id = serializers.PrimaryKeyRelatedField(many=False, queryset = Ingredients.objects.all())

    class Meta:
        model = RecipeIngredients
        fields = ('id', 'amount')

class RecipeIngredientsResponseSerializer(serializers.ModelSerializer):
    name = serializers.SlugRelatedField(many=False, read_only=True, slug_field='name')
    # measurement_unit = MeasurementUnitField(many=True, queryset=RecipeIngredients.objects.all())
    measurement_unit = serializers.CharField(source='name.measurement_unit')

    class Meta:
        model = RecipeIngredients
        fields = ('name_id', 'name', 'measurement_unit','amount')

class TagsSerializer(serializers.ModelSerializer):
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
    # tags = TagsSerializer(required=False, many=True)
    # image = Base64ImageField(required=False, allow_null=True)
    # author = CustomUserSerializer()
    ingredients = RecipeIngredientsSerializer(required=False, many=True)
    
    class Meta:
        model = Recipe
        fields = ('name', 'text', 'cooking_time', 'ingredients')
        # fields = (
        #     'id', 'author', 'tags', 'image', 'name', 'text', 'cooking_time'
        #     )
        # read_only_fields = ('author',)

    def create(self, validated_data):
        if 'ingredients' not in self.initial_data:
            recipe = Recipe.objects.create(**validated_data)
            return recipe
        else:
            ingredients = validated_data.pop('ingredients')
            print(ingredients)
            recipe = Recipe.objects.create(**validated_data)
            for ingredient in ingredients:
                RecipeIngredients.objects.create(
                    recipe=recipe, name=ingredient['id'], amount=ingredient['amount']
                    )
            return recipe
        
    def to_representation(self, data):
        return RecipeResponseSerializer(context=self.context).to_representation(data)
        

class RecipeResponseSerializer(serializers.ModelSerializer):
    # tags = TagsSerializer(required=False, many=True)
    # image = Base64ImageField(required=False, allow_null=True)
    # author = CustomUserSerializer()
    ingredients = RecipeIngredientsResponseSerializer(required=False, many=True)
    
    class Meta:
        model = Recipe
        fields = ('id', 'author', 'ingredients', 'name', 'text', 'cooking_time' )
        read_only_fields = ('author',)



