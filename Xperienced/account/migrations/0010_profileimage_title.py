# Generated by Django 4.2.11 on 2024-06-17 22:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0009_remove_profileimage_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='profileimage',
            name='title',
            field=models.CharField(default='username', max_length=100),
        ),
    ]
