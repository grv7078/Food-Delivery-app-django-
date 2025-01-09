from django.db import models
from django.contrib.auth.models import User
    
class Restaurant(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField()
    phone_number = models.CharField(max_length=15)
    email = models.EmailField()
    image = models.ImageField(upload_to='restaurant_images/', blank=True, null=True)
    cuisine_type = models.CharField(max_length=20, choices=[('indian', 'Indian'), ('chinese', 'Chinese'), ('italian', 'Italian'), ('american', 'American'), ('mexican', 'Mexican')])
    # latitude = models.FloatField()
    # longitude = models.FloatField()

    def __str__(self):
        return self.name    

    
class MenuItem(models.Model):
    restaurant = models.ForeignKey('Restaurant', on_delete=models.CASCADE, related_name='menu_items')
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    category = models.CharField(max_length=50, choices=[('appetizer', 'Appetizer'), ('main', 'Main Course'), ('dessert', 'Dessert')])
    available = models.BooleanField(default=True)  
    
    def __str__(self):
        return self.name
    

class Order(models.Model):
    user_name = models.CharField(max_length=255)
    user_email = models.EmailField()
    user_phone = models.CharField(max_length=15)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    menu_items = models.ManyToManyField(MenuItem, through='OrderItem')
    total_cost = models.DecimalField(max_digits=6, decimal_places=2)
    delivery_address = models.TextField()
    order_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} for {self.user_name}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    
    def __str__(self):
        return f"{self.quantity} x {self.menu_item.name}"   



class OrderTracking(models.Model):
    STATUS_CHOICES = [
        ('PLACED', 'Order Placed'),
        ('PREPARING', 'Preparing'),
        ('OUT_FOR_DELIVERY', 'Out for Delivery'),
        ('DELIVERED', 'Delivered'),
    ]
    
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)  # Link to the user who placed the order
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PLACED')  # Order status
    created_at = models.DateTimeField(auto_now_add=True)  # Time when the order was placed
    updated_at = models.DateTimeField(auto_now=True)  # Time when the order was last updated

    def __str__(self):
        return f"Order {self.id} - {self.get_status_display()}"



class Profile(models.Model):
    # One-to-one relationship with the User model
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    # The device_token field will store the device's unique token for push notifications
    device_token = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.user.username  # Return the username when printing the Profile instance

