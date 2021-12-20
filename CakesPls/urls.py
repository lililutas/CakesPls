"""
Definition of urls for CakesPls.
"""

from datetime import datetime
from django.urls import path
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from app import forms, views


from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings

urlpatterns = [
    path('', views.home, name='home'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('login/',
         LoginView.as_view
         (
             template_name='app/login.html',
             authentication_form=forms.BootstrapAuthenticationForm,
             extra_context=
             {
                 'title': 'Войти',
                 'year' : datetime.now().year,
             }
         ),
         name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('admin/', admin.site.urls),

#Регистрация
    path('registration/', views.registration, name='registration'),

#Новости
    path('news/', views.news, name='news'),
    path('post/<int:postId>/', views.post, name='post'),

#Коммерция
    path('catalog/', views.catalog, name='catalog'),
    path('catalog/<str:cat>/', views.catalog, name='catalog'),
    path('cart/', views.cart, name='cart'),
    path('myOrders/', views.myOrders, name='myOrders'),
    path('allOrders/', views.allOrders, name='allOrders'),
    path('orderDetails/<int:orderId>/', views.orderDetails, name='orderDetails'),


#Действия
    path('deleteItem/', views.deleteItem, name='deleteItem'),
    path('addToCart/', views.addToCart, name='addToCart'),
    path('changeQuantity/', views.changeQuantity, name='changeQuantity'),
    path('dealOrder/', views.dealOrder, name='dealOrder'),
    path('deleteOrder/', views.deleteOrder, name='deleteOrder'),
    path('changeStatus/', views.changeStatus, name='changeStatus'),

]


#Добавление медиа
urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()
