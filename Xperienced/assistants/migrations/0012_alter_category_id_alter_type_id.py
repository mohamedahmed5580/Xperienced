# Generated by Django 4.2.11 on 2024-06-20 10:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assistants', '0011_alter_offer_category_alter_offer_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='id',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='type',
            name='id',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
    ]
