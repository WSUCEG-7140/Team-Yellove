import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from .models import Item, Category, Order, OrderItem, Customer
from django.utils.timezone import make_aware
import datetime
import warnings
import requests

#ISSUE Write unit tests for each API endpoint #30

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


# Import the required pytest module for test marking
import pytest

# Mark this test class as using the Django database
@pytest.mark.django_db
class TestCustomerRegistration:

    # Test to check if authenticated users can access the customers API
    def test_orders_authenticated(self, authenticated_client):
        url = '/restaurant/api/customers/'
        response = authenticated_client.get(url)

        # Assert that the response status code is 200 (OK)
        assert response.status_code == status.HTTP_200_OK

        # Assert that the response content type is JSON
        assert response['content-type'] == 'application/json'

    # Test to check if unauthenticated users are denied access to the customers API
    def test_orders_unauthenticated(self):
        client = APIClient()
        url = '/restaurant/api/customers/'
        response = client.get(url)

        # Assert that the response status code is 401 (Unauthorized)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

        # Assert that the response content type is JSON
        assert response['content-type'] == 'application/json'

    # Test to create a new customer and check if the response is successful
    def test_create_customer(self, authenticated_client):
        url = "/restaurant/api/customers/"
        data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com",
            "phone_number": "1234567890",
            "address": "123 Main Street",
            "date_of_birth": "1990-01-15",
        }

        # Make the POST request to the API endpoint
        response = authenticated_client.post(url, data)

        # Assert that the response status code is 201 (Created) for successful creation
        assert response.status_code == 201

        # Print the JSON response for debugging purposes
        print(response.json())

        # Assert that the customer object is created in the database with the correct details
        assert response.json()['id'] == 1
        assert response.json()['first_name'] == 'John'
        assert response.json()['last_name'] == 'Doe'
        assert response.json()['email'] == 'john.doe@example.com'
    
    # Test to get customers from the API and check the response
    def test_get_customers(self, authenticated_client):
        url = "/restaurant/api/customers/"

        # Create a customer object in the database for testing
        customer = Customer.objects.create(first_name ="John", last_name = "Doe", email = "john.doe@example.com", phone_number = "1234567890", address = "123 Main Street", date_of_birth = "1990-01-15")

        # Make the GET request to the API endpoint
        response = authenticated_client.get(url)

        # Print the JSON response for debugging purposes
        print(response.json())

        # Assert that the response status code is 200 (OK)
        assert response.status_code == 200

        # Assert that the customer object retrieved from the API has the correct details
        assert response.json()[0]['id'] == 1
        assert response.json()[0]['first_name'] == 'John'
        assert response.json()[0]['last_name'] == 'Doe'
        assert response.json()[0]['email'] == 'john.doe@example.com'
    
    # Test to update a customer's details and check the response
    def test_update_customers(self, authenticated_client):
        url = "/restaurant/api/customers/1/"

        # Create a customer object in the database for testing
        customer = Customer.objects.create(first_name ="John", last_name = "Doe", email = "john.doe@example.com", phone_number = "1234567890", address = "123 Main Street", date_of_birth = "1990-01-15")

        # Data containing updated details for the customer
        data = {
            "first_name": "John",
            "last_name": "Reddy",
            "email": "john.doe@google.com",
            "phone_number": "1234567890",
            "address": "123 Main Street",
            "date_of_birth": "1990-01-15"
        }

        # Make the PUT request to the API endpoint
        response = authenticated_client.put(url, data=data)

        # Print the JSON response for debugging purposes
        print(response.json())

        # Assert that the response status code is 200 (OK) for a successful update
        assert response.status_code == 200

        # Assert that the customer object has been updated with the correct details in the response
        assert response.json()['id'] == 1
        assert response.json()['first_name'] == 'John'
        assert response.json()['last_name'] == 'Reddy'
        assert response.json()['email'] == 'john.doe@google.com'
