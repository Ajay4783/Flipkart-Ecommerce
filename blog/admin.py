import os
from django.contrib import admin
from django.core.files import File
from import_export.admin import ImportExportModelAdmin
from .models import *


@admin.action(description='📸 Auto-detect & Update Images')
def auto_update_images(modeladmin, request, queryset):
    base_dir = os.getcwd()
    images_dir = os.path.join(base_dir, 'bulk_images')
    count = 0
    updated_names = []
    
    if not os.path.exists(images_dir):
        modeladmin.message_user(request, "❌ 'bulk_images' folder not found!", level='error')
        return

    
    for item in queryset:
        if item.image:  
            continue
            
        item_name_clean = item.name.lower().strip()
        found = False

        
        for root, dirs, files in os.walk(images_dir):
            for filename in files:
                if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
                    img_name_clean = os.path.splitext(filename)[0].lower().strip()
                    
                    
                    if img_name_clean in item_name_clean or item_name_clean in img_name_clean:
                        try:
                            image_path = os.path.join(root, filename)
                            with open(image_path, 'rb') as f:
                                item.image.save(filename, File(f), save=True)
                                count += 1
                                updated_names.append(item.name)
                                found = True
                                break 
                        except Exception as e:
                            print(f"Error for {item.name}: {e}")
            if found: break
    
    if count > 0:
        modeladmin.message_user(request, f"🎉 Successfully updated {count} images! ({', '.join(updated_names[:3])}..)", level='success')
    else:
        modeladmin.message_user(request, "⚠️ No matching images found for selected items.", level='warning')




@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Product)
class ProductAdmin(ImportExportModelAdmin):
    list_display = ['name', 'category', 'price', 'old_price', 'available', 'image'] 
    list_filter = ['category', 'available']
    list_editable = ['price', 'available']
    search_fields = ['name', 'brand']
    actions = [auto_update_images]  
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
    list_display = ['name', 'brand', 'base_price', 'available', 'image']
    inlines = [FashionVariantInline]
    search_fields = ['name', 'brand']
    actions = [auto_update_images] 

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