from django.contrib import admin
from .models import Product, Order, OrderItem


# ================= PRODUCT ADMIN =================

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):

    list_display = (
        'name',
        'price',
        'category',
        'rating'
    )

    search_fields = (
        'name',
        'category'
    )

    list_filter = (
        'category',
        'rating'
    )


# ================= ORDER ITEM ADMIN =================

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):

    list_display = (
        'product',
        'quantity'
    )


# ================= ORDER ADMIN =================

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):

    list_display = (
        'customer',
        'complete',
        'id'
    )

    list_filter = (
        'complete',
    )

    search_fields = (
        'customer__username',
    )