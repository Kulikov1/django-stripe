from django.contrib import admin

from .models import Item, ItemInOrder, Order


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'description',
        'price',
    )


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
    )


@admin.register(ItemInOrder)
class ItemInOrderAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'order',
        'item',
    )
