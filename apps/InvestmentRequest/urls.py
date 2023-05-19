from django.urls import path

from . import views

urlpatterns = [
    path('main', views.main, name='main'),
    path('details', views.details, name='details'),
    path('update_payback', views.update_payback, name='update_payback'),
    path('login', views.login_InvestmentRequest, name='login_InvestmentRequest'),
    path('logout', views.logout_InvestmentRequest, name='logout_InvestmentRequest'),
]