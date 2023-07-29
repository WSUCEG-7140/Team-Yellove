from django.db import models
# Django Models: https://docs.djangoproject.com/en/4.2/topics/db/models/
""" @ref R12_0"""
#ISSUE: Design the data models and relationships #12
# Define a model for Category

class Category(models.Model):  
    unique_id = models.AutoField(primary_key=True)  # Auto-incrementing primary key
    name = models.CharField(max_length=100)  # Field to store the category name (max length: 100 characters)
    description = models.TextField()  # Field to store the category description (text field)

# Define a model for Item
class Item(models.Model):
    unique_id = models.AutoField(primary_key=True)  # Auto-incrementing primary key
    category = models.ForeignKey(Category, on_delete=models.CASCADE)  # Foreign key to Category model, on deletion cascade
    name = models.CharField(max_length=100)  # Field to store the item name (max length: 100 characters)
    description = models.TextField()  # Field to store the item description (text field)
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Field to store the item price (decimal field) in $.

# Define a model for Ingredient
class Ingredient(models.Model):
    unique_id = models.AutoField(primary_key=True)  # Auto-incrementing primary key
    name = models.CharField(max_length=100)  # Field to store the ingredient name (max length: 100 characters)

# Define a model for Item_Ingredients (M2M relationship between Item and Ingredient)
class Item_Ingredients(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)  # Foreign key to Item model, on deletion cascade
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)  # Foreign key to Ingredient model, on deletion cascade

# Models for Orders

# Define a model for Order
class Order(models.Model):
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('PROCESSING', 'Processing'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    )
    
    unique_id = models.AutoField(primary_key=True)  # Auto-incrementing primary key
    user = models.CharField(max_length=20, null=False)  # Field to store the user (max length: 20 characters)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')  # Field to store the order status
    items = models.ManyToManyField(Item, through='OrderItem')  # Many-to-Many relationship with Item through OrderItem
    created_at = models.DateTimeField(auto_now_add=True)  # Field to store the creation timestamp (auto-filled)
    updated_at = models.DateTimeField(auto_now=True)  # Field to store the last update timestamp (auto-filled)

# Define a model for OrderItem (M2M relationship between Order and Item with additional data)
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)  # Foreign key to Order model, on deletion cascade
    item = models.ForeignKey(Item, on_delete=models.CASCADE)  # Foreign key to Item model, on deletion cascade
    quantity = models.PositiveIntegerField(default=1)  # Field to store the quantity of items in the order (default: 1)

# Define a model for Customer
class Customer(models.Model):
    first_name = models.CharField(max_length=100)  # Field to store the customer's first name (max length: 100 characters)
    last_name = models.CharField(max_length=100)  # Field to store the customer's last name (max length: 100 characters)
    email = models.EmailField()  # Field to store the customer's email address
    phone_number = models.CharField(max_length=15, null=True, blank=True)  # Field to store the customer's phone number
    address = models.TextField(null=True, blank=True)  # Field to store the customer's address (text field)
    date_of_birth = models.DateField(null=True, blank=True)  # Field to store the customer's date of birth
    created_at = models.DateTimeField(auto_now_add=True, null=True)  # Field to store the creation timestamp (auto-filled)

    def __str__(self):
        # Method to return a string representation of the Customer object
        return f"{self.first_name} {self.last_name}"
