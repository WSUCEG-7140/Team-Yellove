from rest_framework import generics
from .models import Item, Order
from .serializers import OrderItemSerializer, OrderSerializer
from rest_framework.response import Response
from rest_framework.views import APIView

class ItemListView(generics.ListAPIView):
    serializer_class = OrderItemSerializer

    def get_queryset(self):
        queryset = Item.objects.all()
        category_id = self.kwargs.get('category_id')
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        return queryset

class OrderListAPIView(generics.ListAPIView):
    serializer_class = OrderSerializer

    def get_queryset(self):
        status_param = self.request.query_params.get('status', None)
        queryset = Order.objects.all()

        if status_param:
            try:
                queryset = queryset.filter(status=status_param)
            except ValueError:
                return Response(
                    {"error": "Invalid status parameter."},
                    status=status.HTTP_400_BAD_REQUEST
                )

        return queryset