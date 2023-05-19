from django.contrib import admin
from .models import ApiLogs

class ApiLogsAdmin(admin.ModelAdmin):
    list_display = ['timestamp', 'customer', 'type', 'name', 'result']

admin.site.register(ApiLogs, ApiLogsAdmin)