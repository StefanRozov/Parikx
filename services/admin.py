from django.contrib import admin
from .models import Service, ServiceCategory

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'duration', 'is_active')
    list_filter = ('category', 'is_active')

admin.site.register(ServiceCategory)