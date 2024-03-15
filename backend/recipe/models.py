from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from . import constants as const

User = get_user_model()


class Ingredients(models.Model):
    name = models.CharField(
        max_length=const.MAX_LENGTH_NAME_CHAR_FIELD,
        verbose_name='ingredient')
    measurement_unit = models.CharField(
        max_length=const.MAX_LENGTH_UNIT_CHAR_FIELD,
        verbose_name='measurement_unit')

    def __str__(self):
        return f'{self.name} ({self.measurement_unit})'


class Tags(models.Model):
    name = models.CharField(
        max_length=const.MAX_LENGTH_NAME_CHAR_FIELD,
        verbose_name='tag')
    color = models.CharField(max_length=const.MAX_LENGTH_COLOR)
    slug = models.SlugField(
        unique=True,
        max_length=const.MAX_LENGTH_SLUG,
        verbose_name='slug'
    )

    class Meta:
        verbose_name = 'tag'
        verbose_name_plural = 'tags'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='author of the recipe',
        blank=False, null=False
    )
    recipe_ingredients = models.ManyToManyField(
        Ingredients, through='RecipeIngredients', related_name='recipes',
        blank=False,
        verbose_name='recipe ingredients')
    tags = models.ManyToManyField(
        Tags, through='TagRecipe', related_name='recipes',
        blank=False,
        verbose_name='recipe tags')
    image = models.ImageField(
        upload_to='recipes/images/',
        blank=False,
        null=False)
    name = models.CharField(
        max_length=const.MAX_LENGTH_NAME_CHAR_FIELD,
        verbose_name='name of the recipe',
        blank=False, null=False)
    text = models.TextField(
        blank=False,
        null=False,
        verbose_name='recipe text')
    cooking_time = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1),
                    MaxValueValidator(const.MAX_COOKING_TIME)],
        blank=False, null=False,)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'recipe'
        verbose_name_plural = 'recipes'

    def __str__(self):
        return self.name

    def clean(self):
        pass
        # if len(self.tags) == 0:
        #     raise ValidationError('At least one address is required.')


class TagRecipe(models.Model):
    tag = models.ForeignKey(Tags, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    def __str__(self):
        return self.tag.name


class RecipeIngredients(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='ingredients',
    )

    name = models.ForeignKey(
        Ingredients,
        on_delete=models.CASCADE,
        related_name='ingredients',
    )

    amount = models.PositiveSmallIntegerField()

    class Meta:
        ordering = ["name"]
        verbose_name = 'ingredient'
        verbose_name_plural = 'ingredients'

    def __str__(self):
        return self.name.name


class Favorites(models.Model):
    user = models.ForeignKey(
        User,
        related_name="favorites",
        on_delete=models.CASCADE)
    recipe = models.ForeignKey(
        Recipe,
        related_name="favorites",
        on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name="unique_favorites")
        ]
        ordering = ["-recipe"]

    def __str__(self):
        f"{self.user} favorites {self.recipe}"


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        User,
        related_name="shopping_cart",
        on_delete=models.CASCADE)
    recipe = models.ForeignKey(
        Recipe,
        related_name="shopping_cart",
        on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name="unique_shopping_cart")
        ]
        ordering = ["-recipe"]

    def __str__(self):
        f"{self.user} add {self.recipe} to shopping cart"
