from django.urls import path

from . import views

urlpatterns = [
    path('db2csv', views.db2csv, name='db2csv'),
    path('aldi_orders', views.aldi_orders, name='aldi_orders'),
    path('aldi_orders_admin', views.aldi_orders_admin, name='aldi_orders_admin'),
]
