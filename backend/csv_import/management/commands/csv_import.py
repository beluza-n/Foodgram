from csv import DictReader
from django.core.management import BaseCommand

from recipe.models import Ingredients


ALREDY_LOADED_ERROR_MESSAGE = """
If you need to reload the reviews data from the CSV file,
first delete the db.sqlite3 file to destroy the database.
Then, run `python manage.py migrate` for a new empty
database with tables"""


class Command(BaseCommand):
    # Показать это, когда пользователь наберет help
    help = "Загружает данные из всех csv-файлов для тестирования приложения"

    def add_arguments(self, parser):
        parser.add_argument('--path', type=str)

    def handle(self, *args, **kwargs):
        path = kwargs['path']
        self.load_ingredients_data(
            filepath='/'.join([path, 'ingredients.csv']))

    def load_ingredients_data(self, filepath):
        # Показать это сообщение, если данные уже есть в БД
        if Ingredients.objects.exists():
            print('Данные по ингридиентам уже загружены...выходим.')
            print(ALREDY_LOADED_ERROR_MESSAGE)
            return

        # Показываем это сообщение перед началом загрузки данных в БД
        print("Загружаем данные по ингридиентам")

        # Загружаем данные в БД
        bulk_list = list()
        for row in DictReader(open(filepath, encoding="utf-8-sig"),
                              fieldnames=['name', 'measurement_unit']):
            ingredient = Ingredients(
                name=row['name'],
                measurement_unit=row['measurement_unit'])
            bulk_list.append(ingredient)
        Ingredients.objects.bulk_create(bulk_list)
