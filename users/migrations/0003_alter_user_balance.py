# Generated by Django 4.1.3 on 2022-12-02 10:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_user_balance'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='balance',
            field=models.FloatField(default=0),
        ),
    ]
