# Generated by Django 5.0.4 on 2024-05-04 12:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("assistantFinder", "0003_user_picture_notification"),
    ]

    operations = [
        migrations.AddField(
            model_name="notification",
            name="read",
            field=models.BooleanField(default=False),
        ),
    ]