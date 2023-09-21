from django.contrib import admin

# Register your models here.
from .models import Client

class ClientAdmin(admin.ModelAdmin):
    list_display = ('clientName', 'province', 'phoneNumber', 'emailAddress', 'date_created')
    search_fields = ('clientName', 'province', 'phoneNumber', 'emailAddress')
    list_filter = ('province',)

admin.site.register(Client, ClientAdmin)
