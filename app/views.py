"""
Definition of views.
"""

from datetime import datetime
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpRequest
from django.contrib.auth.models import User
from django.core.paginator import Paginator

#Импорт форм
from .forms import BootstrapRegistrationForm

#Импорт моделей
from .models import News
from .models import Goods
from .models import Orders
from .models import OrderDetails

#Главная страница

def home(request):
    """Renders the home page."""

    newsPost = News.objects.all()[:6]

    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        {
            'title':'Главная страница',
            'items': newsPost,
            'year':datetime.now().year,
        }
    )


#Контакты


def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title':'Контакты',
            'message':'Свяжитесь с нами тут!',
            'year':datetime.now().year,
        }
    )


#О нас


def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title':'О нас',
            'message':'Позвольте нам представиться',
            'year':datetime.now().year,
        }
    )

#Регистрация

def registration(request):
    """Render the registration page."""
    if request.method == "POST":
        regform = BootstrapRegistrationForm(request.POST)
        if regform.is_valid():
            reg_f = regform.save(commit=False)
            reg_f.is_staff = False
            reg_f.is_active = True
            reg_f.is_superuser = False
            reg_f.date_joined = datetime.now()
            reg_f.last_login = datetime.now()
            regform.save()
            return redirect('home')
    else:
        regform =  BootstrapRegistrationForm()

    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/registration.html',
        {
            'title':'Регистрация',
            'form': regform,
            'year':datetime.now().year,
        }
    )

#Новости

def news(request):
    """Render the news page."""
   
    newsPage = News.objects.all()

    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/news.html',
        {
            'title':'Новости',
            'items': newsPage,
            'year':datetime.now().year,
        }
    )


def post(request, postId):
    """Render the post page."""

    currentPost = News.objects.get(id = postId)

    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/post.html',
        {
            'title':'Пост',
            'item': currentPost,
            'year':datetime.now().year,
        }
    )

#Каталог

def catalog(request, cat = 'all'):
    """Render the catalog page."""
    
    if cat == 'all':
        catalogPage = Goods.objects.all()
    else:
        catalogPage = Goods.objects.filter(category=cat)
    catalogPage = Paginator(catalogPage, 4)
    page = request.GET.get('page')
    catalogPage = catalogPage.get_page(page)
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/catalog.html',
        {
            'title':'Каталог',
            'items': catalogPage,
            'category': cat,
            'year':datetime.now().year,
        }
    )


#Добавление в корзине

def addToCart(request):
    """Add to cart action."""

    current_product = Goods.objects.get(id = request.GET.get('product'))
    current_order, status = Orders.objects.get_or_create(holder=request.user, status='incart')
    if status:
        current_order.save()
    suborder, status = OrderDetails.objects.get_or_create(order=current_order, product=current_product)
    if status: 
        suborder.quantity = 1
        suborder.price = suborder.product.price * suborder.quantity
        suborder.save()
    else:
        suborder.quantity += 1
        suborder.price = suborder.product.price * suborder.quantity
        suborder.save()
    order_list = OrderDetails.objects.filter(order=current_order)
    current_order.total_price = 0
    for item in order_list:
        current_order.total_price += item.price

    current_order.save()
    assert isinstance(request, HttpRequest)
    return redirect(reverse('catalog'))


#Корзина

def cart(request):
    """Render the cart page."""

    currentOrder, status = Orders.objects.get_or_create(holder=request.user, status='incart')
    details = OrderDetails.objects.filter(order=currentOrder)
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/cart.html',
        {
            'title':'Корзина',
            'items': details,
            'order': currentOrder,
            'status': 'cart',
            'year':datetime.now().year,
        }
    )
 
#Удаление товара

def deleteItem(request):
    current_item = OrderDetails.objects.get(id = request.GET.get('item')).delete()
    current_order = Orders.object.get(id = request.GET.get('order'))
    order_list = OrderDetails.objects.filter(order=current_order)
    current_order.total_price = 0
    for item in order_list:
        current_order.total_price += item.price

    current_order.save()
    return redirect(reverse(request.GET.get('next')))

#Изменить колличество

def changeQuantity(request):
    current_item = OrderDetails.objects.get(id = request.GET.get('item'))
    if request.GET.get('action') == 'minus':
        current_item.quantity -= 1
        current_item.price = current_item.product.price * current_item.quantity
    else:
        current_item.quantity += 1
        current_item.price = current_item.product.price * current_item.quantity
    current_item.save()
    current_order = Orders.objects.get(id = request.GET.get('order'))
    order_list = OrderDetails.objects.filter(order=current_order)
    current_order.total_price = 0
    for item in order_list:
        current_order.total_price += item.price

    current_order.save()
    if request.GET.get('next') == 'orderDetails':
        return redirect(request.GET.get('next'), orderId = current_order.id)
    else:
        return redirect(reverse(request.GET.get('next')))

#Сделать заказ

def dealOrder(request):
    current_order = Orders.objects.filter(holder=request.user, status='incart').first()
    current_order.status = 'processed'
    current_order.save()
    
    return redirect(reverse('myOrders'))


def deleteOrder(request):
    current_order = Orders.objects.get(id = request.GET.get('order')).delete()
    return redirect(reverse(request.GET.get('next')))


#Мои заказы

def myOrders(request):
    """Render the myOrders page."""

    currentOrders = Orders.objects.filter(holder=request.user).exclude(status='incart')
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/orders.html',
        {
            'title':'Мои заказы',
            'ordertype':'myOrders',
            'items': currentOrders,
            'year':datetime.now().year,
        }
    )

#Заказы

def allOrders(request):
    """Render the orders page."""

    currentOrders = Orders.objects.all().exclude(status='incart')
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/orders.html',
        {
            'title':'Заказы',
            'ordertype':'allOrders',
            'items': currentOrders,
            'year':datetime.now().year,
        }
    )

#Детали заказа

def orderDetails(request, orderId):
    """Render the details page."""

    currentOrder = Orders.objects.get(id = orderId)
    details = OrderDetails.objects.filter(order=currentOrder)
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/cart.html',
        {
            'title':'Детали заказа',
            'items': details,
            'order': currentOrder,
            'status': 'orderDetails',
            'year':datetime.now().year,
        }
    )







