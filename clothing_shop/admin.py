from django.contrib import admin
from clothing_shop.models import *


@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'crowd_level')
    search_fields = ('name', 'location')


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('name', 'role', 'current_branch')
    list_filter = ('role', 'current_branch')
    search_fields = ('name',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'season', 'fashion_tag')
    list_filter = ('category', 'season')
    search_fields = ('name', 'fashion_tag')


@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ('product', 'branch', 'is_online_warehouse', 'quantity')
    list_filter = ('is_online_warehouse', 'branch')


@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ('product', 'sale_type', 'quantity', 'timestamp', 'branch')
    list_filter = ('sale_type', 'branch')
    date_hierarchy = 'timestamp'


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'event_type', 'start_date', 'end_date')
    list_filter = ('event_type',)
    date_hierarchy = 'start_date'


@admin.register(WebsiteView)
class WebsiteViewAdmin(admin.ModelAdmin):
    list_display = ('product', 'views', 'date')
    date_hierarchy = 'date'
