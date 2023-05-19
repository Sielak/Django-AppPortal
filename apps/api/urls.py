from django.urls import path

from . import views

urlpatterns = [
    path('get_highlight_data', views.get_highlight_data, name='get_highlight_data'),
    path('get_pmoReporting_data', views.get_pmoReporting_data, name='get_pmoReporting_data'),
    path('get_user_data', views.get_user_data, name='get_user_data'),
    path('qr_bill', views.qr_bill, name='qr_bill'),
    path('api_logs', views.api_logs, name='api_logs'),
    path('crossDockingRefresh', views.crossDockingRefresh, name='crossDockingRefresh'),
    path('crossDockingSummaryEmail', views.crossDockingSummaryEmail, name='crossDockingSummaryEmail'),
    path('cab_refresh', views.cab_refresh, name='cab_refresh'),
    path('track_and_trace', views.track_and_trace, name='track_and_trace'),
]
