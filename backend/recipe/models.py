from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth import get_user_model

User = get_user_model()


class Tag(models.Model):
    name = models.CharField(max_length=256, verbose_name='tag')
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
    name = models.CharField(max_length=256, verbose_name='name of the recipe')
    # image 
    text = models.TextField(
        blank=False,
        null=False,
        verbose_name='recipe text')
    tag = models.ManyToManyField(
        Tag, related_name='recipes',
        blank=False,
        null=False,
        verbose_name='recipe tags')



    year = models.IntegerField(
        validators=[title_year_validation, ],
        blank=False,
        null=False,
        verbose_name='release year')
    description = models.TextField(
        blank=True,
        null=True,
        default='',
        verbose_name='title of the work')
    genre = models.ManyToManyField(
        Genre, related_name='titles',
        blank=True,
        verbose_name='genre of the work')
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL,
        related_name='titles', blank=True, null=True,
        verbose_name='category of the work')

    class Meta:
        ordering = ["name"]
        verbose_name = 'title'
        verbose_name_plural = 'titles'

    def __str__(self):
        return self.name
