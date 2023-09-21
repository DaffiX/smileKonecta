from django.contrib import admin

# Register your models here.
from .models import *

class ClientAdmin(admin.ModelAdmin):
    list_display = ('clientName', 'province', 'phoneNumber', 'emailAddress', 'date_created')
    search_fields = ('clientName', 'province', 'phoneNumber', 'emailAddress')
    list_filter = ('province',)

class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'quantity', 'price', 'currency', 'invoice', 'date_created', 'last_updated')
    list_filter = ('currency', 'date_created')
    search_fields = ('title', 'description', 'invoice__invoice_number')
    prepopulated_fields = {'slug': ('title',)}

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('number', 'dueDate', 'status', 'client')
    list_filter = ('status',)
    # Add other customizations for the admin interface if needed.


admin.site.register(Client, ClientAdmin)
admin.site.register(Product, ProductAdmin)
