from django.core.management import BaseCommand
from django.contrib.auth import get_user_model

from django.conf import settings

User = get_user_model()


class Command(BaseCommand):

    def handle(self, *args, **options):
        User.objects.create_user(
            username=settings.DJANGO_SUPERUSER_USERNAME,
            email=settings.DJANGO_SUPERUSER_EMAIL,
            password=settings.DJANGO_SUPERUSER_PASSWORD,
            first_name=settings.DJANGO_SUPERUSER_FIRST_NAME,
            last_name=settings.DJANGO_SUPERUSER_LAST_NAME,
            is_staff=True,
            is_active=True,
            is_superuser=True
        )

        User.objects.create_user(
            username='ivan',
            email='ivanov@mail.ru',
            password='Changeme1!',
            first_name='Ivan',
            last_name='Ivanov',
            is_staff=False,
            is_active=True,
            is_superuser=False
        )

        User.objects.create_user(
            username='peter',
            email='petrov@mail.ru',
            password='Changeme1!',
            first_name='Peter',
            last_name='Petrov',
            is_staff=False,
            is_active=True,
            is_superuser=False
        )
