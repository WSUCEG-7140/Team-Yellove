from rest_framework import generics
from .models import Item, Order, OrderItem
from .serializers import ItemSerializer, CreateOrderSerializer, ViewOrderSerializer, UpdateItemSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets


class ItemListView(generics.ListAPIView):
    serializer_class = ItemSerializer

    def get_queryset(self):
        queryset = Item.objects.all()
        category_id = self.kwargs.get('category_id')
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        return queryset

class OrderCreateAPIView(APIView):
    def post(self, request, format=None):
        serializer = CreateOrderSerializer(data=request.data)
        if serializer.is_valid():
            order = serializer.save()

            response_data = {
                'order_id' : order.unique_id,
                'user': order.user,
                'status': order.status,
                'items': []
            }

            for order_item in order.orderitem_set.all():
                item_data = {
                    'name': order_item.item.name,
                    'quantity': order_item.quantity
                }
                response_data['items'].append(item_data)

            return Response(response_data, status=201)
        return Response(serializer.errors, status=400)


class ListOrdersAPIView(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = ViewOrderSerializer



from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Order, OrderItem, Item

@api_view(['POST'])
def add_or_update_order_item(request, order_id):
    try:
        order = Order.objects.get(unique_id=order_id)
    except Order.DoesNotExist:
        return Response({'message': 'Order does not exist'}, status=404)
    
    items = request.data.get('items', [])
    
    for item_data in items:
        item_id = item_data.get('item')
        quantity = item_data.get('quantity', 1)
        
        item, _ = Item.objects.get_or_create(unique_id=item_id)
        
        order_item, created = OrderItem.objects.get_or_create(order=order, item=item)
        order_item.quantity = quantity
        order_item.save()
    
    return Response({'message': 'Items added/updated successfully'}, status=200)


