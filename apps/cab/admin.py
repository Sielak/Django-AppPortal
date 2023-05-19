from django.contrib import admin
from .models import CabData


class CabDataAdmin(admin.ModelAdmin):
    list_display = ['id','status','step','stream','feature','est_dev_hrs','est_cost_sek', 'est_deliv_date', 'subject','hl_payer']
    
    
admin.site.register(CabData, CabDataAdmin)
