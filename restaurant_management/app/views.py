# Import necessary modules
from rest_framework import generics  #FOr generics: https://docs.djangoproject.com/en/4.2/topics/class-based-views/generic-display/
from .models import Item, Order, OrderItem, Customer
from .serializers import ItemSerializer, CreateOrderSerializer, ViewOrderSerializer, UpdateItemSerializer, CustomerSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets
from django.db.models import Q
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.decorators import action
# FOr rest+framework: https://www.django-rest-framework.org/

# ISSUE Add Search Functionality for Menu Items #22
""" @ref R22_0"""
# Apply the 'IsAuthenticated' permission class to the following views
@permission_classes([IsAuthenticated])
class ItemListView(generics.ListAPIView):
    # Define the serializer class for this view
    serializer_class = ItemSerializer

    def get_queryset(self):
        # Retrieve all items from the database
        queryset = Item.objects.all()
        # Get the 'category_id' from the URL's keyword arguments
        category_id = self.kwargs.get('category_id')
        if category_id:
            # If 'category_id' is provided, filter the items based on it
            queryset = queryset.filter(category_id=category_id)

        # Get the 'search' query parameter from the request
        search_query = self.request.GET.get('search', None)
        if search_query:
            # If 'search' query parameter is provided, filter the items based on name containing the search query
            queryset = queryset.filter(Q(name__icontains=search_query))

        return queryset

# ISSUE API endpoints for Placing an order #21
""" @ref R21_0"""
@permission_classes([IsAuthenticated])
class OrderCreateAPIView(APIView):
    # Handle POST requests to create an order
    def post(self, request, format=None):
        serializer = CreateOrderSerializer(data=request.data)
        if serializer.is_valid():
            # If the data is valid, save the order and its related items
            order = serializer.save()

            response_data = {
                'order_id': order.unique_id,
                'user': order.user,
                'status': order.status,
                'items': []
            }

            for order_item in order.orderitem_set.all():
                # Collect item data for each item in the order
                item_data = {
                    'name': order_item.item.name,
                    'quantity': order_item.quantity
                }
                response_data['items'].append(item_data)

            return Response(response_data, status=201)
        # If data is invalid, return errors with 400 status code
        return Response(serializer.errors, status=400)

#ISSUE 14 API endpoints for Tracking order status #14
""" @ref R14_0"""
@permission_classes([IsAuthenticated])
class ListOrdersAPIView(generics.ListAPIView):
    # Display a list of all orders
    queryset = Order.objects.all()
    serializer_class = ViewOrderSerializer

# Define a view function to add or update items in an order
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Order, OrderItem, Item


# ISSUE API endpoints for Adding items to the order #20
""" @ref R20_0"""
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_or_update_order_item(request, order_id):
    try:
        # Get the order using the 'order_id' provided in the URL
        order = Order.objects.get(unique_id=order_id)
    except Order.DoesNotExist:
        return Response({'message': 'Order does not exist'}, status=404)

    # Get the list of items from the request data
    items = request.data.get('items', [])

    for item_data in items:
        # For each item in the request data, extract 'item_id' and 'quantity'
        item_id = item_data.get('item')
        quantity = item_data.get('quantity', 1)

        # Get or create the Item instance based on 'item_id'
        item, _ = Item.objects.get_or_create(unique_id=item_id)

        # Get or create the OrderItem instance based on the order and item
        order_item, created = OrderItem.objects.get_or_create(order=order, item=item)
        # Set the quantity for the OrderItem and save it
        order_item.quantity = quantity
        order_item.save()

    return Response({'message': 'Items added/updated successfully'}, status=200)

""" @ref R29_0"""
# ISSUE API endpoints for Customer registration #29
# Define a viewset for Customer model
class CustomerViewSet(viewsets.ModelViewSet):
    # Display a list of all customers and allow CRUD operations
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticated]  # Add the permission class here

    @action(detail=True, methods=['GET'])
    def get_customer_details(self, request, pk=None):
        # Display details of a specific customer using the 'pk' provided in the URL
        customer = self.get_object()
        serializer = self.get_serializer(customer)
        return Response(serializer.data)

    def perform_create(self, serializer):
        # Save the newly created customer instance
        serializer.save()
