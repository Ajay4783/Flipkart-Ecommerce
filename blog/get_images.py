import os
import requests
import re
import time
import random


products = [
"T-shirt",
"Men Regular Fit Polo T-Shirt",
"Women Floral Print Maxi Dress",
"Men Slim Fit Denim Jeans",
"Unisex Running Sports Shoes",
"Women Cotton Printed Kurta Set",
"Men Formal Cotton Shirt",
"Women Textured Leather Handbag",
"Unisex Aviator Sunglasses",
"Vintage Series Digital Watch",
"Men Winter Hooded Sweatshirt",
"Casual Canvas Sneakers",
"Men Traditional Ethnic Kurta",
"Genuine Leather Bi-fold Wallet",
"Men Printed Resort Shirt",
"Men Slim Fit Cargo Pants",
"Women Block Heel Sandals",
"Women Cotton Track Pants",
"Men Denim Trucker Jacket",
"Travel Laptop Backpack 30L",
"Unisex Cotton Baseball Cap",
"Women A-Line Midi Dress",
"Men Chino Trousers",
"Women Silk Blend Saree",
"Men Round Neck Graphic Tee",
"Women High Waist Jeans",
"Unisex Slide Sandals",
"Men Bomber Jacket",
"Women Tote Bag",
"Men Sports Shorts",
"Women Georgette Anarkali Suit",
]


base_dir = "bulk_images"
save_dir = os.path.join(base_dir, "fashion")
if not os.path.exists(save_dir):
    os.makedirs(save_dir)


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}

print("🚀 Downloading Images from Bing (Direct Mode)...")

for product in products:
    
    
    search_query = product.split('(')[0].strip()
    
    print(f"🔍 Searching: {search_query}...")
    
    try:
        
        url = f"https://www.bing.com/images/search?q={search_query}&first=1"
        
        
        response = requests.get(url, headers=headers)
        html = response.text
        
        
        
        links = re.findall('murl&quot;:&quot;(.*?)&quot;', html)
        
        if links:
            img_url = links[0] 
            
            
            img_data = requests.get(img_url, headers=headers, timeout=10).content
            
            
            safe_name = "".join([c for c in product if c.isalnum() or c in (' ', '-', '_')]).strip()
            file_path = os.path.join(save_dir, f"{safe_name}.jpg")
            
            with open(file_path, 'wb') as f:
                f.write(img_data)
            print(f"✅ Saved: {file_path}")
        else:
            print(f"⚠️ No images found for {search_query}")

    except Exception as e:
        print(f"❌ Error: {e}")

    
    time.sleep(1.5)

print("🎉 All Done! Check 'bulk_images' folder!")