# Generated by Django 3.2.16 on 2024-03-09 13:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='customuser',
            options={'ordering': ['email'], 'verbose_name': 'user', 'verbose_name_plural': 'users'},
        ),
    ]