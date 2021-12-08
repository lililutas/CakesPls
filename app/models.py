"""
Definition of models.
"""

from django.db import models

# Create your models here.


from datetime import datetime
from django.contrib import admin
from django.contrib.auth.models import User


#Профиль
class Profile(models.Model):
	USERROLE = (
		('client', 'Клиент'),
		('moderator', 'Модератор'),
		('admin', 'Администратор'),
		)

#Поля

	user = models.ForeignKey(User, on_delete = models.CASCADE, verbose_name = 'Пользователь')
	role = models.CharField(max_length = 300, choices = USERROLE, verbose_name = 'Роль пользователя')


	def __str__(self):
		return 'Профиль'

#БД

	class Meta:
		db_table = 'Profile'
		ordering = ['user']
		verbose_name = 'Профиль'
		verbose_name_plural = 'Профиль'

#Новости

class News(models.Model):

#Поля

	title = models.CharField(max_length = 100, verbose_name = 'Заголовок')
	description =  models.CharField(max_length = 200, verbose_name = 'Краткое содержание')
	content = models.TextField(verbose_name = 'Полное содержание')
	posted = models.DateTimeField(default = datetime.now(), db_index = True, verbose_name = 'Опубликовано')
	image = models.FileField(default = 'temp.jpg', verbose_name = 'Путь к картинке')

	def __str__(self):
		return self.title

#БД

	class Meta:
			db_table = 'News'
			ordering = ['posted']
			verbose_name = 'Новости'
			verbose_name_plural = 'Новости'



#Товары

class Goods(models.Model):

	CATEGORY = (
		('cat_1', 'Торты'),
		('cat_2', 'Пироги'),
		('cat_3', 'Пирожные'),
		('cat_4', 'Печенье'),
		)

#Поля

	name = models.TextField(verbose_name = 'Название товара')
	short = models.TextField(verbose_name = 'Краткое описание', max_length = 200)
	text = models.TextField(verbose_name = 'Описание товара')
	price = models.IntegerField(verbose_name = 'Цена')
	category = models.CharField(verbose_name = 'Категория', max_length = 300, choices = CATEGORY)
	image = models.FileField(default = 'temp.jpg', verbose_name = 'Путь к картинке')


	def __str__(self):
		return 'Товар %s: %s' % (self.id, self.name)

#БД

	class Meta:
		db_table = 'Goods'
		ordering = ['id']
		verbose_name = 'Товары'
		verbose_name_plural = 'Товары'
										 
#Заказы

class Orders(models.Model):
	STATUS = (
		('incart', 'В корзине'),
		('processed', 'Обрабатывается'),
		('intransit', 'Доставляется'),
		('delivered', 'Доставлен')
	)

#Поля

	holder = models.ForeignKey(User, on_delete = models.CASCADE, verbose_name = 'Покупатель')
	status = models.CharField(verbose_name = 'Статус', choices = STATUS, max_length=300)
	total_price = models.IntegerField(default = 0, verbose_name = 'Итоговая стоимость')


	def __str__(self):
		return 'Заказ %s' % (self.id)

#БД

	class Meta:
		db_table = 'Orders'
		ordering = ['holder']
		verbose_name = 'Заказы'
		verbose_name_plural = 'Заказы'


#Детали заказа

class OrderDetails(models.Model):

#Поля

	order = models.ForeignKey(Orders, on_delete = models.CASCADE, verbose_name = 'Заказ')
	product = models.ForeignKey(Goods, on_delete = models.CASCADE, verbose_name = 'Товар')
	quantity = models.IntegerField(default = 1, verbose_name = 'Количество')
	price = models.IntegerField(default = 0, verbose_name = 'Стоимость товаров')
	


	def __str__(self):
		return 'Товар %s к заказу %s' % (self.product, self.order)

#БД

	class Meta:
		db_table = 'OrderDetails'
		ordering = ['order']
		verbose_name = 'Детали заказа'
		verbose_name_plural = 'Детали заказа'

#Добавление БД в административный раздел

admin.site.register(Profile)
admin.site.register(News)
admin.site.register(Goods)
admin.site.register(Orders)
admin.site.register(OrderDetails)




