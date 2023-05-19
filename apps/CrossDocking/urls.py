from django.urls import path

from . import views

urlpatterns = [
    path('main', views.cross_docking, name='main_crossDocking'),
    path('login', views.login_crossDocking, name='login_crossDocking'),
    path('logout', views.logout_crossDocking, name='logout_crossDocking'),
]
