from django.contrib import admin
from django.utils.html import format_html
from .models import Restaurant, MenuItem, Order, OrderItem, Profile, OrderTracking

@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'image_tag', 'phone_number')
    search_fields = ('name', 'address', 'phone_number')
    readonly_fields = ('image_tag',)

    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width: 45px; height: 45px;" />'.format(obj.image.url))
        return "No Image"
    image_tag.short_description = 'Image'


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'available', 'restaurant')
    search_fields = ('name', 'category')
    list_filter = ('category', 'available')
    list_editable = ('price', 'available')


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1  # Number of empty forms to display in the admin for adding items

class OrderAdmin(admin.ModelAdmin):
    list_display = ('user_name', 'restaurant', 'total_cost', 'order_date', 'delivery_address')
    search_fields = ('user_name', 'user_email', 'restaurant__name', 'order_date')
    list_filter = ('order_date', 'restaurant')
    inlines = [OrderItemInline]

    def get_order_total(self, obj):
        return obj.total_cost
    get_order_total.short_description = 'Total Cost'

admin.site.register(Order, OrderAdmin)


class OrderTrackingAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'status', 'created_at', 'updated_at')  
    list_filter = ('status', 'created_at')  
    search_fields = ('user__username', 'status') 
    ordering = ('-created_at',) 
    
admin.site.register(OrderTracking, OrderTrackingAdmin)



# Register Profile model to the admin interface
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'device_token')  
    search_fields = ('user__username',)  
    list_filter = ('user',)  

admin.site.register(Profile, ProfileAdmin)
