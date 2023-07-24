import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from .models import Item, Category

CustomUser = get_user_model()

# Fixture to create an authenticated client with a user
@pytest.fixture
def authenticated_client():
    # Create a new CustomUser instance with the specified email and password
    user = CustomUser.objects.create_user(email='testuser@example.com', password='testpassword')
    # Create an instance of APIClient
    client = APIClient()
    # Forcefully authenticate the client with the created user
    client.force_authenticate(user=user)
    return client

# Fixture to create categories and items in the database
@pytest.fixture
def create_categories_and_items():
    # Create two categories
    category1 = Category.objects.create(name="Appetizers", description="A collection of appetizers.")
    category2 = Category.objects.create(name="Appetizers2", description="A collection of appetizers.")

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
        assert len(response.json()) == 1  # There should be one item in the response
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