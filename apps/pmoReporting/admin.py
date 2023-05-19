from django.contrib import admin
from .models import Entity, Profile, PmoData, Category, SubCategory

class ProfileAdmin(admin.ModelAdmin):
    filter_horizontal = ('user_group',)
    raw_id_fields = ("user",)
    list_display = ('user', 'get_email')

    def get_email(self, obj):
        return obj.user.email
    get_email.short_description = 'User Email'
    get_email.admin_order_field = 'user__email'

class PmoDataAdmin(admin.ModelAdmin):
    list_display = ['location', 'location_type', 'initiative_type', 'initiative_product']
    readonly_fields=('creation_date',)
    fields = (('location', 'location_type', 'initiative_type'),
              ('category', 'subcategory'),
              ('initiative_product', 'status'),
              ('implementation_deadline', "initiative_year", "creation_date"),
              ('actual_01', 'budget_01'),
              ('actual_02', 'budget_02'),
              ('actual_03', 'budget_03'),
              ('actual_04', 'budget_04'),
              ('actual_05', 'budget_05'),
              ('actual_06', 'budget_06'),
              ('actual_07', 'budget_07'),
              ('actual_08', 'budget_08'),
              ('actual_09', 'budget_09'),
              ('actual_10', 'budget_10'),
              ('actual_11', 'budget_11'),
              ('actual_12', 'budget_12')
              )

admin.site.register(Profile, ProfileAdmin)
admin.site.register(Entity)
admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(PmoData, PmoDataAdmin)