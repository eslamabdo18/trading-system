# Generated by Django 4.1.3 on 2022-12-03 17:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PendingOrders',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('order_type', models.IntegerField(choices=[(1, 'Buy'), (2, 'Sell')])),
                ('total', models.IntegerField()),
                ('upper_bound', models.FloatField()),
                ('lower_bound', models.FloatField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('stock_id', models.CharField(max_length=500, unique=True)),
                ('name', models.CharField(max_length=150, unique=True)),
                ('price', models.FloatField()),
                ('availability', models.IntegerField()),
                ('timestamp', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='StockStream',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('price', models.FloatField()),
                ('availability', models.IntegerField()),
                ('timestamp', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='UserStock',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('buy_price', models.FloatField()),
                ('total_count', models.FloatField()),
                ('stock', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='users_stock', to='stocks.stock')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
