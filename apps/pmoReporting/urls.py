from django.urls import path

from . import views

urlpatterns = [
    path('main', views.pmoReporting, name='main_pmoReporting'),
    path('login', views.login_pmoReporting, name='login_pmoReporting'),
    path('logout', views.logout_pmoReporting, name='logout_pmoReporting'),
]
