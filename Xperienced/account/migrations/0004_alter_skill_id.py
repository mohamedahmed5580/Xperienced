# Generated by Django 4.2.11 on 2024-06-15 21:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_alter_skill_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='skill',
            name='id',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
    ]
