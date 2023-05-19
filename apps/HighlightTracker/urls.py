from django.urls import path

from . import views

urlpatterns = [
    path('main', views.highlight_tracker, name='main_HighlightTracker'),
    path('login', views.login_HighlightTracker, name='login_HighlightTracker'),
    path('logout', views.logout_HighlightTracker, name='logout_HighlightTracker'),
]
