from django.core.management import BaseCommand
from django.contrib.auth import get_user_model
import os
from dotenv import load_dotenv 

load_dotenv()

User = get_user_model()

DJANGO_SUPERUSER_USERNAME = os.getenv('DJANGO_SUPERUSER_USERNAME', 'admin1')
DJANGO_SUPERUSER_EMAIL = os.getenv('DJANGO_SUPERUSER_EMAIL', 'admin1@mail.ru')
DJANGO_SUPERUSER_PASSWORD = os.getenv('DJANGO_SUPERUSER_PASSWORD', '1234')
DJANGO_SUPERUSER_FIRST_NAME = os.getenv('DJANGO_SUPERUSER_FIRST_NAME', 'admin1')
DJANGO_SUPERUSER_LAST_NAME = os.getenv('DJANGO_SUPERUSER_LAST_NAME', 'admin1')

class Command(BaseCommand):


    def handle(self, *args, **options):
        User.objects.create_user(
            username=DJANGO_SUPERUSER_USERNAME,
            email=DJANGO_SUPERUSER_EMAIL,
            password=DJANGO_SUPERUSER_PASSWORD,
            first_name=DJANGO_SUPERUSER_FIRST_NAME,
            last_name=DJANGO_SUPERUSER_LAST_NAME,
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
