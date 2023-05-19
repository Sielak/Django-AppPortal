from django.contrib import admin
from .models import CrossDockingLogs, CrossDockingParams

class CrossDockingParamsAdmin(admin.ModelAdmin):
    list_display = ['Param_Name', 'Param_Value_int', 'Param_Value_string']

class CrossDockingLogsAdmin(admin.ModelAdmin):
    list_display = ['po_number', 'delivery_number', 'file_uploaded']

admin.site.register(CrossDockingLogs, CrossDockingLogsAdmin)
admin.site.register(CrossDockingParams, CrossDockingParamsAdmin)
