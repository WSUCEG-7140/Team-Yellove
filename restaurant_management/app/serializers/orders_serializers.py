from rest_framework import serializers
from ..models import Order, OrderItem, Item


class CreateItemSerializer(serializers.Serializer):
    unique_id = serializers.IntegerField()
    quantity = serializers.IntegerField()

class CreateOrderSerializer(serializers.Serializer):
    user = serializers.CharField()
    items = CreateItemSerializer(many=True)

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        order = Order.objects.create(**validated_data)

        for item_data in items_data:
            item_id = item_data.pop('unique_id')
            quantity = item_data.pop('quantity')
            item = Item.objects.get(unique_id=item_id)
            OrderItem.objects.create(order=order, item=item, quantity=quantity)

        return order

class ViewOrderSerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ['unique_id', 'user', 'status', 'items', 'created_at', 'updated_at']

    def get_items(self, obj):
        items_data = []
        order_items = obj.orderitem_set.all()

        for order_item in order_items:
            item_data = {
                'name': order_item.item.name,
                'quantity': order_item.quantity
            }
            items_data.append(item_data)

        return items_data


