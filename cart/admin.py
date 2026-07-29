from django.contrib import admin
from .models import Order, ContactMessage, Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'price', 'stock', 'discount', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name', 'description', 'color']
    list_editable = ['price', 'stock', 'discount']
    ordering = ['-created_at']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        'id', 
        'full_name', 
        'email', 
        'phone', 
        'total', 
        'created_at',
    ]
    
    list_filter = [
        'created_at',
    ]
    
    search_fields = [
        'first_name',
        'last_name',
        'email',
        'phone',
    ]
    
    ordering = ['-created_at']
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return True  
    
    def full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"
    full_name.short_description = 'Customer Name'
    
    fieldsets = (
        ('Customer Information', {
            'fields': ('first_name', 'last_name', 'email', 'phone', 'address', 'city')
        }),
        ('Order Details', {
            'fields': ('items_data_pretty', 'total', 'created_at')
        }),
    )
    
    readonly_fields = ['items_data_pretty', 'total', 'created_at']
    
    def items_data_pretty(self, obj):
        import json
        items = json.loads(obj.items_data)
        if not items:
            return "No items."
        lines = []
        for item in items:
            lines.append(
                f"{item['name']} × {item['quantity']} = ${item['subtotal']}"
            )
        return "\n".join(lines)
    items_data_pretty.short_description = 'Items'

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'email', 'phone', 'message_preview', 'created_at']
    
    search_fields = ['name', 'email', 'phone', 'message']
    
    list_filter = ['created_at']
    
    ordering = ['-created_at']
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return True
    
    def message_preview(self, obj):
        if len(obj.message) > 50:
            return obj.message[:50] + '...'
        return obj.message
    message_preview.short_description = 'Message'
    
    fieldsets = (
        ('Sender Information', {
            'fields': ('name', 'email', 'phone')
        }),
        ('Message Details', {
            'fields': ('message', 'created_at')
        }),
    )
    
    readonly_fields = ['name', 'email', 'phone', 'message', 'created_at']