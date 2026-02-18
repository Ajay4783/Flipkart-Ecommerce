from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import *

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Product)
class ProductAdmin(ImportExportModelAdmin):
    list_display = ['name', 'category', 'price', 'old_price', 'available']
    list_filter = ['category', 'available']
    list_editable = ['price', 'available']
    search_fields = ['name', 'brand']
    fieldsets = (
        ('Basic Information', {'fields': ('category', 'name', 'brand', 'image')}),
        ('Pricing', {'fields': ('price', 'old_price', 'available')}),
        ('Details', {'fields': ('description', 'specification')}),
    )

class FashionVariantInline(admin.TabularInline):
    model = FashionVariant
    extra = 1

@admin.register(FashionItem)
class FashionItemAdmin(ImportExportModelAdmin):
    list_display = ['name', 'brand', 'base_price', 'available']
    inlines = [FashionVariantInline]
    search_fields = ['name', 'brand']

@admin.register(Flight)
class FlightAdmin(ImportExportModelAdmin):
    list_display = ['airline', 'flight_number', 'source', 'destination', 'departure_time', 'price']
    list_filter = ['airline', 'source', 'destination']
    search_fields = ['airline', 'source', 'destination', 'flight_number']

@admin.register(ReviewRating)
class ReviewRatingAdmin(admin.ModelAdmin):
    list_display = ['product', 'user', 'subject', 'rating', 'status', 'created_at']
    list_filter = ['status', 'rating']
    search_fields = ['product__name', 'user__username', 'subject']

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['product', 'fashion_item', 'quantity', 'price']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'total_price', 'status', 'is_paid', 'created_at']
    list_filter = ['status', 'is_paid', 'created_at'] 
    list_editable = ['status', 'is_paid']
    inlines = [OrderItemInline]

admin.site.register(OrderItem)