from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2) 
    old_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True) 
    brand = models.CharField(max_length=100, null=True, blank=True)
    image = models.ImageField(upload_to='products/')
    description = models.TextField()
    specification = models.JSONField(null=True, blank=True) 
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    

class FashionItem(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='fashion_products')
    name = models.CharField(max_length=200)
    brand = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    material = models.CharField(max_length=100, blank=True) 
    image = models.ImageField(upload_to='fashion/')
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.brand} - {self.name}"
    


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True) 
    
    fashion_item = models.ForeignKey(FashionItem, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.product:
            return f"{self.user.username} - {self.product.name}"
        elif self.fashion_item:
            return f"{self.user.username} - {self.fashion_item.name}"
        return "Unknown Item"
    
    @property
    def total_cost(self):
        if self.product:
            return self.quantity * self.product.price
        elif self.fashion_item:
            return self.quantity * self.fashion_item.base_price
        return 0

class Order(models.Model):
    STATUS = (
        ('Order Placed', 'Order Placed'),
        ('Accepted', 'Accepted'),
        ('Shipped', 'Shipped'),
        ('Out for Delivery', 'Out for Delivery'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'), 
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_price = models.FloatField()
    address = models.TextField(null=True, blank=True)
    
    is_paid = models.BooleanField(default=False)
    payment_method = models.CharField(max_length=100, default='Cash on Delivery')

    status = models.CharField(max_length=50, choices=STATUS, default='Order Placed')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    fashion_item = models.ForeignKey(FashionItem, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.IntegerField(default=1)
    price = models.FloatField()
    
    def __str__(self):
        return f"Item in Order {self.order.id}"


class FashionVariant(models.Model):
    SIZE_CHOICES = (
        ('All', 'All'),
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
        ('XL', 'Extra Large'),
        ('XXL', 'Double Extra Large'),
    )
    product = models.ForeignKey(FashionItem, on_delete=models.CASCADE, related_name='variants')
    size = models.CharField(max_length=5, choices=SIZE_CHOICES)
    color = models.CharField(max_length=50)
    stock = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return f"{self.product.name} ({self.size} - {self.color})"


class Flight(models.Model):
    airline = models.CharField(max_length=100) 
    flight_number = models.CharField(max_length=20)
    source = models.CharField(max_length=100) 
    destination = models.CharField(max_length=100) 
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration = models.CharField(max_length=20, null=True, blank=True) 
    image = models.ImageField(upload_to='airlines/', null=True, blank=True) 

    def __str__(self):
        return f"{self.airline} - {self.source} to {self.destination}"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mobile = models.CharField(max_length=15, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return self.user.username
    

class ReviewRating(models.Model):
    
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)

    fashion_item = models.ForeignKey(FashionItem, on_delete=models.CASCADE, null=True, blank=True)
    
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    subject = models.CharField(max_length=100, blank=True)
    review = models.TextField(max_length=500, blank=True)
    rating = models.FloatField()
    ip = models.CharField(max_length=20, blank=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject


class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    fashion_item = models.ForeignKey(FashionItem, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Wishlist ({self.user.username})"