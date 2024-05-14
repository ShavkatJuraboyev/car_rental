from django.contrib import admin
from .models import AdminProfile
# Register your models here.

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_admin', 'is_self_visible')
    list_filter = ('is_admin', 'is_self_visible')
    search_fields = ('user__username', 'user__email')


admin.site.register(AdminProfile, ProfileAdmin)