from django.contrib import admin
from .models import Area, Group, SubjectGroup, \
highlight_data, Profile, Country, highlight_tracker_settings

class highlight_dataAdmin(admin.ModelAdmin):
    list_display = ['id', 'Subject_Group', 'Improvement_Identified', 'Action_description', 'Responsible_person',
                    'Completion_Date', 'Action_status', 'Comments', 'row_Group', 'row_Area', 'row_country', 'row_Year']

class ProfileAdmin(admin.ModelAdmin):
    filter_horizontal = ('user_group', 'user_area', 'user_country')
    raw_id_fields = ("user",)
    list_display = ('__str__', 'get_email')

    def get_email(self, obj):
        return obj.user.email
    get_email.short_description = 'User Email'
    get_email.admin_order_field = 'user__email'

class highlight_tracker_settingsAdmin(admin.ModelAdmin):
    list_display = ['Name', 'Value']

admin.site.register(Area)
admin.site.register(Group)
admin.site.register(SubjectGroup)
admin.site.register(highlight_data, highlight_dataAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Country)
admin.site.register(highlight_tracker_settings, highlight_tracker_settingsAdmin)

