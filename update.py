import os
import django


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Ecommerce.settings')
django.setup()

from django.core.files import File
from blog.models import Product


base_dir = os.getcwd()
images_dir = os.path.join(base_dir, 'bulk_images', 'Tv and Appliances')

print(f"🚀 Starting update process...")
print(f"📂 Reading images from: {images_dir}")

if os.path.exists(images_dir):
    files = os.listdir(images_dir)
    
    count = 0
    for filename in files:
        if filename.endswith(('.jpg', '.jpeg', '.png', '.webp')):
            
            clean_name = os.path.splitext(filename)[0]
            clean_name = clean_name.split('(')[0].strip()

            print(f"🔍 Processing: '{clean_name}'...")
            
            
            matches = Product.objects.filter(name__icontains=clean_name)
            
            
            if not matches.exists():
                words = clean_name.split()
                if len(words) >= 2:
                    short_name = f"{words[0]} {words[1]}"
                    matches = Product.objects.filter(name__icontains=short_name)

            
            if matches.exists():
                for product in matches:
                    if not product.image:
                        image_path = os.path.join(images_dir, filename)
                        with open(image_path, 'rb') as f:
                            product.image.save(filename, File(f), save=True)
                            print(f"✅ Updated: {product.name}")
                            count += 1
                    else:
                        print(f"⚡ Skipped (Already has image): {product.name}")
            else:
                print(f"❌ No match found for: {clean_name}")

    print(f"\n🎉 Total Products Updated: {count}")

else:
    print("⚠️ Folder not found! 'bulk_images/electronics' ஃபோல்டர் இருக்கான்னு பாருங்க.")