from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Shop)
admin.site.register(Category)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Product)
admin.site.register(ShippingAddress)
admin.site.register(ShopOrder)

class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email')

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'email') 
