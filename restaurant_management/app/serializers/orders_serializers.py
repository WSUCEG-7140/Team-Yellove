from rest_framework import serializers
from ..models import Order, OrderItem, Item
#For Serializer : #https://www.django-rest-framework.org/api-guide/serializers/

# Serializer for the 'Item' model when creating an order
class CreateItemSerializer(serializers.Serializer):
    unique_id = serializers.IntegerField()  # Integer field for the 'unique_id' of the Item
    quantity = serializers.IntegerField()  # Integer field for the quantity of the Item in the order

# Serializer for updating 'OrderItem' model
class UpdateItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem  # Define the model to be serialized
        fields = ['item', 'quantity']  # Specify the fields to include in the serialized representation

    def update(self, instance, validated_data):
        # Update the 'quantity' field of the 'OrderItem' instance with the new validated data
        instance.quantity = validated_data.get('quantity', instance.quantity)
        instance.save()
        return instance

    def to_internal_value(self, data):
        # This method is used to convert the external representation of the data to internal values
        item_id = data.get('item_id')  # Get the 'item_id' from the data
        try:
            # Retrieve the Item object using the 'item_id'
            item = Item.objects.get(unique_id=item_id)
        except Item.DoesNotExist:
            raise serializers.ValidationError(f"Item with unique_id '{item_id}' does not exist.")
        return {
            'item': item,
            'quantity': data.get('quantity')  # Get the 'quantity' from the data
        }

# Serializer for creating an 'Order' model
class CreateOrderSerializer(serializers.Serializer):
    user = serializers.CharField()  # Char field for the 'user' who placed the order
    items = CreateItemSerializer(many=True)  # Nested serializer for 'Item' data, representing multiple items in the order

    def create(self, validated_data):
        # Create an Order object with the validated data
        items_data = validated_data.pop('items')  # Get the 'items' data from the validated data
        order = Order.objects.create(**validated_data)

        # Create 'OrderItem' objects for each item in the order
        for item_data in items_data:
            item_id = item_data.pop('unique_id')  # Get the 'unique_id' of the item
            quantity = item_data.pop('quantity')  # Get the 'quantity' of the item
            item = Item.objects.get(unique_id=item_id)  # Get the Item object using 'item_id'
            OrderItem.objects.create(order=order, item=item, quantity=quantity)  # Create the OrderItem

        return order

# Serializer for viewing an 'Order' model
class ViewOrderSerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField()  # Custom method to get the items in the order

    class Meta:
        model = Order  # Define the model to be serialized
        fields = ['unique_id', 'user', 'status', 'items', 'created_at', 'updated_at']  # Specify the fields to include in the serialized representation

    def get_items(self, obj):
        # Custom method to retrieve the items and their quantities for the order
        items_data = []
        order_items = obj.orderitem_set.all()  # Get all OrderItem objects associated with this order

        # Create a list of dictionaries with 'name' and 'quantity' for each item in the order
        for order_item in order_items:
            item_data = {
                'name': order_item.item.name,
                'quantity': order_item.quantity
            }
            items_data.append(item_data)

        return items_data
