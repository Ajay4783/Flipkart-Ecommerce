import os
import django

# 1. Django-வை செட் செய்கிறோம் (இது இருந்தால் தான் தனியா ரன் ஆகும்)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Ecommerce.settings')
django.setup()

from django.core.files import File
from blog.models import Product

# 2. போட்டோக்கள் இருக்கும் இடம்
base_dir = os.getcwd()
images_dir = os.path.join(base_dir, 'bulk_images', 'Grocerry')

print(f"🚀 Starting update process...")
print(f"📂 Reading images from: {images_dir}")

if os.path.exists(images_dir):
    files = os.listdir(images_dir)
    
    count = 0
    for filename in files:
        if filename.endswith(('.jpg', '.jpeg', '.png', '.webp')):
            # பெயர் சுத்தம் செய்தல்
            clean_name = os.path.splitext(filename)[0]
            clean_name = clean_name.split('(')[0].strip()

            print(f"🔍 Processing: '{clean_name}'...")
            
            # --- முயற்சி 1: முழுப் பெயரை வைத்துத் தேடுதல் ---
            matches = Product.objects.filter(name__icontains=clean_name)
            
            # --- முயற்சி 2: கிடைக்கவில்லை என்றால், முதல் 2 வார்த்தைகள் ---
            if not matches.exists():
                words = clean_name.split()
                if len(words) >= 2:
                    short_name = f"{words[0]} {words[1]}"
                    matches = Product.objects.filter(name__icontains=short_name)

            # --- அப்டேட் செய்தல் ---
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