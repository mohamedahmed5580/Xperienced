# Generated by Django 4.2.11 on 2024-06-19 10:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('assistants', '0005_alter_category_name_alter_type_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='user',
        ),
        migrations.RemoveField(
            model_name='type',
            name='user',
        ),
    ]
