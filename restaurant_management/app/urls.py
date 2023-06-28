from django.urls import path
from .views import ItemListView, OrderListAPIView

urlpatterns = [
    # Other URL patterns in your project
    path('items/', ItemListView.as_view(), name='item-list'),
    path('items/category/<int:category_id>/', ItemListView.as_view(), name='item-list-filtered'),
    path('orders/', OrderListAPIView.as_view(), name='order-list'),
]