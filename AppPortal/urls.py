"""AppPortal URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

def trigger_error(request):
    division_by_zero = 1 / 0

handler500 = 'apps.converters.views.handler500'
urlpatterns = [
    path('admin/', admin.site.urls),
    path('sentry-debug/', trigger_error),
    path('api/', include('apps.api.urls')),
    path('cab/', include('apps.cab.urls')),
    path('converters/', include('apps.converters.urls')),
    path('CrossDocking/', include('apps.CrossDocking.urls')),
    path('HighlightTracker/', include('apps.HighlightTracker.urls')),
    path('pmoReporting/', include('apps.pmoReporting.urls')),
    path('InvestmentRequest/', include('apps.InvestmentRequest.urls')),
]
