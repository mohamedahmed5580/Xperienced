# Generated by Django 4.2.11 on 2024-06-19 09:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('assistants', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='category', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='type',
            name='name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='type',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='type', to=settings.AUTH_USER_MODEL),
        ),
    ]
