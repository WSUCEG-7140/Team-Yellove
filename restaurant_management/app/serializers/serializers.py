# Import necessary modules
from rest_framework import serializers
from ..models import Item, Category, Order, OrderItem, Customer
#For Serializer : https://www.django-rest-framework.org/api-guide/serializers/

# Serializer for Category model
class CategorySerializer(serializers.ModelSerializer):  
    class Meta:
        model = Category  # Define the model to be serialized
        fields = ('unique_id', 'name', 'description')  # Specify the fields to include in the serialized representation

# Serializer for Item model
class ItemSerializer(serializers.ModelSerializer):
    # Create additional fields 'category_name' and 'category_id' by accessing data from related Category model
    category_name = serializers.CharField(source='category.name')  # 'category.name' accesses the 'name' field in the related Category model
    category_id = serializers.CharField(source='category.unique_id')  # 'category.unique_id' accesses the 'unique_id' field in the related Category model

    class Meta:
        model = Item  # Define the model to be serialized
        fields = ('unique_id', 'name', 'category_name', 'category_id', 'price', 'description')
        # Specify the fields to include in the serialized representation,
        # including the additional fields 'category_name' and 'category_id'

# Serializer for Customer model
class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer  # Define the model to be serialized
        fields = '__all__'
        # '__all__' includes all fields from the Customer model in the serialized representation
