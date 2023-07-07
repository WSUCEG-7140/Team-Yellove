from django.urls import path
from .views import ItemListView

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OrderCreateAPIView, ListOrdersAPIView

# router = DefaultRouter()
# router.register(r'get_orders', OrderViewSet)
# router.register(r'create_order',CreateOrderViewSet)

urlpatterns = [
    # Other URL patterns in your 
    # path('', include(router.urls)),
    path('items/', ItemListView.as_view(), name='item-list'),
    path('items/category/<int:category_id>/', ItemListView.as_view(), name='item-list-filtered'),
    path('orders/create/', OrderCreateAPIView.as_view(), name='order-create'),
    path('orders/', ListOrdersAPIView.as_view(), name='list_orders'),
]
