# Generated by Django 4.1.4 on 2022-12-06 22:19

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('stocks', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userstock',
            name='total_count',
            field=models.IntegerField(),
        ),
        migrations.AlterUniqueTogether(
            name='userstock',
            unique_together={('user', 'stock')},
        ),
    ]