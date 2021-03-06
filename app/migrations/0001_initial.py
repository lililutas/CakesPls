# Generated by Django 2.2.25 on 2021-12-08 07:30

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Заголовок')),
                ('description', models.CharField(max_length=200, verbose_name='Краткое содержание')),
                ('content', models.TextField(verbose_name='Полное содержание')),
                ('posted', models.DateTimeField(db_index=True, default=datetime.datetime(2021, 12, 8, 10, 30, 52, 319483), verbose_name='Опубликовано')),
                ('image', models.FileField(default='temp.jpg', upload_to='', verbose_name='Путь к картинке')),
            ],
        ),
        migrations.CreateModel(
            name='Shop',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(verbose_name='Название товара')),
                ('short', models.TextField(max_length=200, verbose_name='Краткое описание')),
                ('text', models.TextField(verbose_name='Описание товара')),
                ('price', models.IntegerField(verbose_name='Цена')),
                ('category', models.CharField(choices=[('cat_1', 'Торты'), ('cat_2', 'Пироги'), ('cat_3', 'Пирожные'), ('cat_4', 'Печенье')], max_length=300, verbose_name='Категория')),
                ('image', models.FileField(default='temp.jpg', upload_to='', verbose_name='Путь к картинке')),
            ],
            options={
                'verbose_name': 'Товары',
                'verbose_name_plural': 'Товары',
                'db_table': 'Goods',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(choices=[('client', 'Клиент'), ('moderator', 'Модератор'), ('admin', 'Администратор')], max_length=300, verbose_name='Роль пользователя')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Профиль',
                'verbose_name_plural': 'Профиль',
                'db_table': 'Profile',
                'ordering': ['user'],
            },
        ),
        migrations.CreateModel(
            name='Orders',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('incart', 'В корзине'), ('processed', 'Обрабатывается'), ('intransit', 'Доставляется'), ('delivered', 'Доставлен')], max_length=300, verbose_name='Статус')),
                ('total_price', models.IntegerField(default=0, verbose_name='Итоговая стоимость')),
                ('holder', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Покупатель')),
            ],
            options={
                'verbose_name': 'Заказы',
                'verbose_name_plural': 'Заказы',
                'db_table': 'Orders',
                'ordering': ['holder'],
            },
        ),
        migrations.CreateModel(
            name='OrderDetails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=1, verbose_name='Количество')),
                ('price', models.IntegerField(default=0, verbose_name='Стоимость товаров')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Orders', verbose_name='Заказ')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Shop', verbose_name='Товар')),
            ],
            options={
                'verbose_name': 'Детали заказа',
                'verbose_name_plural': 'Детали заказа',
                'db_table': 'OrderDetails',
                'ordering': ['order'],
            },
        ),
    ]
