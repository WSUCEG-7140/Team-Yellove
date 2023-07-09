from rest_framework import serializers
from ..models import Item, Category, Order, OrderItem

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('unique_id', 'name', 'description')

class ItemSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name')
    category_id = serializers.CharField(source='category.unique_id')

    class Meta:
        model = Item
        fields = ('unique_id','name', 'category_name','category_id', 'price', 'description')

