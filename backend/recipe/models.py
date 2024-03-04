from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth import get_user_model

User = get_user_model()


class Ingredients(models.Model):
    name = models.CharField(max_length=256, verbose_name='ingredient')
    measurement_unit = models.CharField(max_length=16, verbose_name='measurement unit')

class Tags(models.Model):
    name = models.CharField(max_length=256, verbose_name='tag')
    color = models.CharField(max_length=16)
    slug = models.SlugField(
        unique=True,
        max_length=50,
        verbose_name='slug'
    )

    class Meta:
        verbose_name = 'tag'
        verbose_name_plural = 'tags'

    def __str__(self):
        return self.slug

class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='author of the recipe'
    )
    tags = models.ManyToManyField(
        Tags, related_name='recipes',
        blank=True,
        null=True,
        verbose_name='recipe tags')
    image = models.ImageField(
        upload_to='recipes/images/', 
        blank=True,
        null=True
        )
    name = models.CharField(max_length=200, verbose_name='name of the recipe')
    text = models.TextField(
        blank=False,
        null=False,
        verbose_name='recipe text')
    cooking_time = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1),])


    class Meta:
        ordering = ["name"]
        verbose_name = 'title'
        verbose_name_plural = 'titles'

    def __str__(self):
        return self.name

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
        verbose_name = 'ingredients'
        verbose_name_plural = 'ingredients'

    def __str__(self):
        return self.name


