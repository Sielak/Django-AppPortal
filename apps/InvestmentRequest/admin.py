from django import forms
from django.contrib import admin
from .models import CashFlowNames, Companies, CashFlowGroupNames, InvestmentHeader, InvestmentRow, ApprovalData, Attachments

class CashFlowNamesAdmin(admin.ModelAdmin):
    list_display = ['row_number', 'name', 'cash_flow_group']

class AttachmentsAdmin(admin.ModelAdmin):
    list_display = ['header', 'name']
    @admin.display()
    def header(self, obj):
        return obj.header.name

class CompaniesAdmin(admin.ModelAdmin):
    list_display = ['number', 'name']
    raw_id_fields = (
        "approval_level_1",
        "approval_level_2",
        "approval_level_3",
        "approval_level_4",
        "approval_level_5",
        "approval_level_6",
        "approval_level_7",
        "approval_level_8",
        "approval_level_9",
        )
    fields = (
        ('name', 'number'),
        ('approval_level_1_desc', 'approval_level_1'),
        ('approval_level_2_desc', 'approval_level_2'),
        ('approval_level_3_desc', 'approval_level_3'),
        ('approval_level_4_desc', 'approval_level_4'),
        ('approval_level_5_desc', 'approval_level_5'),
        ('approval_level_6_desc', 'approval_level_6'),
        ('approval_level_7_desc', 'approval_level_7'),
        ('approval_level_8_desc', 'approval_level_8'),
        ('approval_level_9_desc', 'approval_level_9'),
    )

class InvestmentHeaderAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at', 'updated_at')
    list_display = ['name', 'created_at', 'updated_at']
    fields = (
        ('name', 'company', 'project'),
        ('requested_amount', 'depreciation_date'),
        ('created_by', 'created_at'),
        ('updated_by', 'updated_at'),
         'why', 'what', 'how', 'alternative', 'env_impact', 
    )

admin.site.register(CashFlowNames, CashFlowNamesAdmin)
admin.site.register(Companies, CompaniesAdmin)
admin.site.register(CashFlowGroupNames)
admin.site.register(InvestmentHeader, InvestmentHeaderAdmin)
admin.site.register(InvestmentRow)
admin.site.register(ApprovalData)
admin.site.register(Attachments, AttachmentsAdmin)
