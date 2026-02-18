import os
import requests
import re
import time
import random


products = [
    "Fortune Chakki Fresh Atta 5kg",
    "India Gate Basmati Rice 5kg",
    "Tata Salt 1kg",
    "Saffola Gold Refined Oil 1L",
    "Madhur Pure Sugar 1kg",
    "Tata Sampann Toor Dal 1kg",
    "Catch Turmeric Powder 200g",
    "Everest Red Chilli Powder 200g",
    "MDH Garam Masala 100g",
    "Dhara Kachi Ghani Mustard Oil 1L",
    "Daawat Rozana Rice 5kg",
    "Kabuli Chana 1kg",
    "Rajma Chitra 1kg",
    "Fortune Sunflower Oil 1L",
    "Moong Dal 1kg",
    "Aashirvaad Multigrain Atta 5kg",
    "Catch Black Pepper 100g",
    "Everest Meat Masala 100g",
    "Goldiee Hing 50g",
    "24 Mantra Organic Poha 500g",
    "Maggi 2-Minute Noodles 420g",
    "Parle-G Gold Biscuits 800g",
    "Britannia Good Day Cashew 200g",
    "Haldiram Bhujia Sev 400g",
    "Lay's Classic Salted Chips 50g",
    "Kurkure Masala Munch 90g",
    "Hide & Seek Choco Chips 120g",
    "Sunfeast Dark Fantasy 100g",
    "Oreo Vanilla Sandwich 120g",
    "Amul Dark Chocolate 150g",
    "Cadbury Dairy Milk Pack 130g",
    "Bikano Aloo Bhujia 400g",
    "Kellogg's Corn Flakes 475g",
    "Baggry's Muesli 500g",
    "Kwality Walls Vanilla 700ml",
    "McCain French Fries 450g",
    "Top Ramen Curry Noodles 280g",
    "Bingo Mad Angles 80g",
    "Act II Popcorn Butter 60g",
    "Paper Boat Peanut Chikki 150g",
    "Tata Tea Gold 500g",
    "Nescafe Classic Coffee 50g",
    "Bru Instant Coffee 100g",
    "Brooke Bond Red Label 500g",
    "Bournvita Health Drink 500g",
    "Horlicks Health Drink 500g",
    "Complan Chocolate 500g",
    "Tropicana Orange Juice 1L",
    "Real Mixed Fruit Juice 1L",
    "Coca-Cola 1.25L Bottle",
    "Amul Masti Buttermilk 1L",
    "Paper Boat Aam Panna 250ml",
    "Red Bull Energy Drink 250ml",
    "Amul Cow Ghee 1L Tin",
    "Mother Dairy Butter 500g",
    "Dabur Honey 500g",
    "Kissan Mixed Fruit Jam 700g",
    "Peanut Butter Creamy 500g",
    "Nutella Hazelnut Spread 350g",
    "Amul Cheese Slices 200g",
    "Dettol Antiseptic Liquid 500ml",
    "Lifebuoy Total Soap 125g",
    "Dove Cream Bar 125g",
    "Pears Pure & Gentle 125g",
    "Head & Shoulders Shampoo 340ml",
    "Pantene Pro-V Shampoo 340ml",
    "Parachute Coconut Oil 500ml",
    "Bajaj Almond Drops 200ml",
    "Nivea Soft Cream 200ml",
    "Pond's Talcum Powder 400g",
    "Colgate MaxFresh Gel 150g",
    "Sensodyne Fresh Mint 150g",
    "Oral-B Soft Toothbrush",
    "Gillette Mach 3 Razor",
    "Old Spice After Shave 150ml",
    "Whisper Ultra Clean 15 Pads",
    "Stayfree Secure XL 20 Pads",
    "Vaseline Body Lotion 400ml",
    "Fair & Lovely Cream 80g",
    "Park Avenue Deodorant 150ml",
    "Surf Excel Matic Liquid 2kg",
    "Ariel Matic Top Load 2kg",
    "Tide Plus Jasmine & Rose 2kg",
    "Comfort Fabric Conditioner 860ml",
    "Lizol Floor Cleaner 2L",
    "Harpic Toilet Cleaner 1L",
    "Vim Dishwash Bar Combo",
    "Scotch-Brite Scrub Pad",
    "Colin Glass Cleaner 500ml",
    "Godrej aer Pocket 10g",
    "Odonil Room Spray 240ml",
    "Hit Flying Insect Spray 400ml",
    "Mortein Mosquito Coil",
    "All Out Ultra Refill Pack",
    "Selpak Toilet Tissue 4 Rolls",
    "Origami Kitchen Towels",
    "Gala Floor Mop",
    "Ziploc Food Storage Bags",
    "Freshwrap Silver Foil 72m",
    "Duracell AA Batteries 4pcs",
]


base_dir = "bulk_images"
save_dir = os.path.join(base_dir, "grocerry")
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