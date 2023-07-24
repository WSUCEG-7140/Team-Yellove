# from django.urls import reverse
# from rest_framework import status
# from rest_framework.test import APITestCase
# from djoser.conf import settings as djoser_settings  # Import Djoser settings
# from .models import Item
# from .serializers import ItemSerializer

# class ItemListViewTestCase(APITestCase):
#     def setUp(self):
#         # Create test items
#         self.category_id = 1
#         self.item1 = Item.objects.create(name='Item 1', category_id=self.category_id, price=10, description='Description 1')
#         self.item2 = Item.objects.create(name='Item 2', category_id=self.category_id, price=20, description='Description 2')

#         # Create a test user with Djoser
#         self.user_data = {
#             'username': 'testuser',
#             'password': 'testpassword',
#         }
#         self.user = djoser_settings.get('SERIALIZERS')['user'].create_user(**self.user_data)

#     # Rest of the test cases remain unchanged


#     def get_token(self):
#         # Get the JWT token using Djoser endpoint
#         url = reverse('token_obtain_pair')  # Replace with your Djoser token endpoint
#         data = {
#             'username': self.user_data['username'],
#             'password': self.user_data['password'],
#         }
#         response = self.client.post(url, data)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         return response.data['access']

#     def test_item_list_view(self):
#         # Test authenticated access with JWT token
#         token = self.get_token()
#         self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
#         url = reverse('item-list', kwargs={'category_id': self.category_id})
#         response = self.client.get(url)

#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         expected_data = ItemSerializer(Item.objects.filter(category_id=self.category_id), many=True).data
#         self.assertEqual(response.data, expected_data)

#     def test_item_list_view_unauthenticated(self):
#         # Test unauthenticated access
#         url = reverse('item-list', kwargs={'category_id': self.category_id})
#         response = self.client.get(url)

#         self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

#     def test_item_serializer(self):
#             item_data = {
#                 'unique_id': 'item-unique-id',
#                 'name': 'Test Item',
#                 'category_name': 'Test Category',
#                 'category_id': 'test-category-id',
#                 'price': 15,
#                 'description': 'Test description',
#             }
#             serializer = ItemSerializer(data=item_data)

#             self.assertTrue(serializer.is_valid())
#             item_instance = serializer.save()

#             self.assertEqual(item_instance.name, item_data['name'])
#             self.assertEqual(item_instance.category.name, item_data['category_name'])
#             self.assertEqual(item_instance.category.unique_id, item_data['category_id'])
#             self.assertEqual(item_instance.price, item_data['price'])
#             self.assertEqual(item_instance.description, item_data['description'])

