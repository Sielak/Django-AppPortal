from django.urls import path

from . import views

urlpatterns = [
    path('main', views.cab_list, name='cab_list'),
]
