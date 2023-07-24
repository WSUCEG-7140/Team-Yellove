import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from .models import Item, Category, Order, OrderItem
from django.utils.timezone import make_aware
import datetime
import warnings
# Add this line to ignore the DeprecationWarning
warnings.filterwarnings("ignore", category=DeprecationWarning)

CustomUser = get_user_model()

# Fixture to create an authenticated client with a user


@pytest.fixture
def authenticated_client():
    # Create a new CustomUser instance with the specified email and password
    user = CustomUser.objects.create_user(
        email='testuser@example.com', password='testpassword')
    # Create an instance of APIClient
    client = APIClient()
    # Forcefully authenticate the client with the created user
    client.force_authenticate(user=user)
    return client

# Fixture to create categories and items in the database


@pytest.fixture
def create_categories_and_items():
    # Create two categories
    category1 = Category.objects.create(
        name="Appetizers", description="A collection of appetizers.")
    category2 = Category.objects.create(
        name="Appetizers2", description="A collection of appetizers.")

    # Create two items belonging to the respective categories
    appetizer1 = Item.objects.create(
        category=category1,
        unique_id=1,
        name="Bruschetta",
        description="Toasted bread topped with fresh tomatoes, basil, and garlic.",
        price=8.99
    )

    appetizer2 = Item.objects.create(
        category=category2,
        unique_id=2,
        name="Caprese Salad",
        description="Tomatoes, fresh mozzarella, and basil drizzled with balsamic glaze.",
        price=9.99
    )

# Mark the test class to use the Django database and ignore deprecation warnings


@pytest.mark.filterwarnings("ignore::DeprecationWarning")
@pytest.mark.django_db
class TestRestaurantAPIItems:

    # Test to check if authenticated users can access the items API
    def test_items_authenticated(self, authenticated_client):
        url = '/restaurant/api/items/'
        response = authenticated_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response['content-type'] == 'application/json'

    # Test to check if unauthenticated users are denied access to the items API
    def test_items_unauthenticated(self):
        client = APIClient()
        url = '/restaurant/api/items/'
        response = client.get(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response['content-type'] == 'application/json'

    # Test to get items by category for authenticated users
    def test_get_items_by_category_with_auth(self, authenticated_client, create_categories_and_items):
        url = '/restaurant/api/items/category/1/'
        response = authenticated_client.get(url)
        assert response.status_code == 200
        # There should be one item in the response
        assert len(response.json()) == 1
        assert response.json()[0]['name'] == 'Bruschetta'

    # Test to get items by category where no items are found
    def test_get_appetizers_not_found(self, authenticated_client):
        url = '/restaurant/api/items/category/3/'
        response = authenticated_client.get(url)
        assert response.status_code == 200
        assert response.json() == []

    # Test to search for items and check if the correct item is found
    def test_search_appetizers_not_found(self, authenticated_client, create_categories_and_items):
        url = '/restaurant/api/items/?search=Salad'
        response = authenticated_client.get(url)
        assert response.status_code == 200
        assert response.json() == [{'unique_id': 2, 'name': 'Caprese Salad', 'category_name': 'Appetizers2', 'category_id': '2',
                                    'price': '9.99', 'description': 'Tomatoes, fresh mozzarella, and basil drizzled with balsamic glaze.'}]


@pytest.fixture
def create_orders():
    # Create a test order and related items

    category1 = Category.objects.create(
        name="Appetizers", description="A collection of appetizers.")
    category2 = Category.objects.create(
        name="Appetizers2", description="A collection of appetizers.")

    # Create two items belonging to the respective categories
    item1 = Item.objects.create(
        category=category1,
        unique_id=1,
        name="Bruschetta",
        description="Toasted bread topped with fresh tomatoes, basil, and garlic.",
        price=8.99
    )

    item2 = Item.objects.create(
        category=category2,
        unique_id=2,
        name="Caprese Salad",
        description="Tomatoes, fresh mozzarella, and basil drizzled with balsamic glaze.",
        price=9.99
    )
    order = Order.objects.create(
        unique_id=1,
        user='John',
        status='PENDING',
        created_at=make_aware(datetime.datetime(2023, 7, 7, 10, 0, 0)),
        updated_at=make_aware(datetime.datetime(2023, 7, 7, 10, 15, 0))
    )

    OrderItem.objects.create(order=order, item=item1, quantity=1)
    OrderItem.objects.create(order=order, item=item2, quantity=2)


@pytest.fixture
def order_request_data():
    return {
        "user": "Pravallika",
        "items": [
            {
                "unique_id": 1,
                "quantity": 2
            },
            {
                "unique_id": 2,
                "quantity": 1
            }
        ]
    }


@pytest.mark.django_db
class TestRestaurantOrders:

    # Test to check if authenticated users can access the items API
    def test_orders_authenticated(self, authenticated_client):
        url = 'http://localhost:8000/restaurant/api/orders/'
        response = authenticated_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response['content-type'] == 'application/json'

        # Test to check if unauthenticated users are denied access to the items API
    def test_orders_unauthenticated(self):
        client = APIClient()
        url = 'http://localhost:8000/restaurant/api/orders/'
        response = client.get(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response['content-type'] == 'application/json'

    # Test to get items by category for authenticated users
    def test_get_orders_by_category_with_auth(self, authenticated_client, create_orders):
        url = 'http://localhost:8000/restaurant/api/orders/'
        response = authenticated_client.get(url)
        assert response.status_code == 200
        # There should be one item in the response
        assert len(response.json()) == 1
        print(response.json())
        assert response.json()[0]['user'] == 'John'
        assert response.json()[0]['status'] == 'PENDING'
        assert response.json()[0]['items'] == [{'name': 'Bruschetta', 'quantity': 1}, {
            'name': 'Caprese Salad', 'quantity': 2}]

    def test_create_order(self, authenticated_client, order_request_data, create_orders):
        # Assuming you have a URL name for the order creation API
        url = "/restaurant/api/orders/create/"

        # Perform a POST request to create the order with the request data from the fixture
        response = authenticated_client.post(
            url, data=order_request_data, format='json')

        # Assert the status code
        assert response.status_code == status.HTTP_201_CREATED

        print(response.json())

        # Assert the response data
        assert response.data == {'order_id': 2, 'user': 'Pravallika', 'status': 'PENDING', 'items': [
            {'name': 'Bruschetta', 'quantity': 2}, {'name': 'Caprese Salad', 'quantity': 1}]}

    def test_update_order(self, authenticated_client, create_orders):
        # Assuming you have a URL name for the order creation API
        url = "/restaurant/api/orders/1/items/"

        order_request_data = {
            "items": [
                {
                    "item": 1,
                    "quantity": 2
                }
            ]
        }

        # Perform a POST request to create the order with the request data from the fixture
        response = authenticated_client.post(
            url, data=order_request_data, format='json')

        # Assert the status code
        assert response.status_code == status.HTTP_200_OK

        print(response.json())

        # Assert the response data
        assert response.data == {"message": "Items added/updated successfully"}
