from django.urls import path
from .views import ItemListView

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OrderCreateAPIView, ListOrdersAPIView, add_or_update_order_item, CustomerViewSet
# for rest_framework https://www.django-rest-framework.org/

router = DefaultRouter()
router.register(r'customers', CustomerViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('items/', ItemListView.as_view(), name='item-list'),
    path('items/category/<int:category_id>/', ItemListView.as_view(), name='item-list-filtered'),
    path('orders/create/', OrderCreateAPIView.as_view(), name='order-create'),
    path('orders/', ListOrdersAPIView.as_view(), name='list_orders'),
    path('orders/<int:order_id>/items/', add_or_update_order_item, name='add_or_update_order_item')
]