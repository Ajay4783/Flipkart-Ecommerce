import os
import django
from django.core.files import File
import random


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Ecommerce.settings')
django.setup()

from blog.models import Product, FashionItem, Category

def run_upload():
    print("🚀 Starting Bulk Upload Process...")

    
    
    print("🗑️ Deleting old products...")
    Product.objects.all().delete()
    FashionItem.objects.all().delete()
    print("✅ Old data deleted.")

    base_dir = os.getcwd()
    images_dir = os.path.join(base_dir, 'bulk_images')

    if not os.path.exists(images_dir):
        print(f"❌ Error: '{images_dir}' folder not found!")
        return

    count = 0

    
    for root, dirs, files in os.walk(images_dir):
        folder_name = os.path.basename(root).lower() 

        
        category_obj = None
        
        
        is_fashion = 'fashion' in folder_name

        if not is_fashion and folder_name != 'bulk_images':
            
            category_obj, created = Category.objects.get_or_create(name=folder_name.capitalize(), slug=folder_name)

        for filename in files:
            if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
                try:
                    
                    product_name = os.path.splitext(filename)[0].replace('_', ' ').replace('-', ' ').title()
                    
                    image_path = os.path.join(root, filename)
                    
                    
                    if is_fashion:
                        item = FashionItem(
                            name=product_name,
                            brand="Generic",
                            base_price=random.randint(500, 3000), 
                            available=True,
                            description=f"High quality {product_name} for men and women."
                        )
                        with open(image_path, 'rb') as f:
                            item.image.save(filename, File(f), save=True)
                        print(f"👗 Added Fashion: {product_name}")

                    
                    elif category_obj:
                        item = Product(
                            name=product_name,
                            category=category_obj,
                            brand="Generic",
                            price=random.randint(5000, 50000), 
                            available=True,
                            description=f"Latest model {product_name} with amazing features."
                        )
                        with open(image_path, 'rb') as f:
                            item.image.save(filename, File(f), save=True)
                        print(f"📱 Added Product: {product_name}")
                    
                    count += 1

                except Exception as e:
                    print(f"❌ Error adding {filename}: {e}")

    print(f"\n🎉 SUCCESS! Total Products Added: {count}")

if __name__ == '__main__':
    run_upload()