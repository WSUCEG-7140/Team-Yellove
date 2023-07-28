# Team-Yellove


# Restaurant Management Application

# Setting up the Project with Docker and Git Clone

1. Clone the Git repository using the following command: `git clone https://github.com/WSUCEG-7140/Team-Yellove.git`. This will download the repository to your local machine, and it will be stored in a folder named "Team-Yellove."

2. Build and run the Docker environment by executing the command: `docker-compose up --build`. Docker Compose will orchestrate the services defined in the `docker-compose.yml` file from the cloned repository. The `--build` flag instructs Docker to rebuild the images if they are outdated or if changes have been made to the Dockerfile.

Before running these commands, ensure that you have Git and Docker (with Docker Compose) installed on your system. Additionally, navigate to the correct directory (the one containing the `docker-compose.yml` file) before executing the `docker-compose up` command.

#Main code
The main code will be in views.py,models.py and serializer folder. We need to check all the folders which are having these names for the code.


# API Documentation

## 1. User Registration: POST http://localhost:8000/auth/users/

### Description:
This API endpoint allows you to create a new user with the provided details.

### Authentication:
Authentication is not required to access this endpoint.
### Request:

#### Method: POST

**Endpoint:** `/auth/users/`

**Headers:**
```json
{
    "Content-Type": "application/json"
}
```

**Body:**
```json
{
    "email": "pravallika@example.com",
    "first_name": "prava",
    "last_name": "allika",
    "password": "Create@123"
}
```

### Response:

#### Success Response:
**Code:** 200 OK
**Sample Output:**

```json
{
    "first_name": "prava",
    "last_name": "allika",
    "email": "pravallika@example.com",
    "id": 7
}
```


## 2. Authenticate User: POST http://localhost:8000/auth/jwt/create

### Description:
This API endpoint allows you to obtain JWT (JSON Web Tokens) for user authentication.

### Authentication:
Authentication is not required to access this endpoint.

### Request:

#### Method: POST

**Endpoint:** `/auth/jwt/create`

**Headers:**
```json
{
    "Content-Type": "application/json"
}
```

**Body:**
```json
{
    "email": "pravallika@example.com",
    "password": "Create@123"
}
```

### Response:

#### Success Response:
**Code:** 200 OK
**Sample Output:**
```json
{
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY5MDM3MjM2NCwianRpIjoiNTA4ODU4YzRjMGNiNGM0ODlmMTJlZGZjMWFiNjQ2NjQiLCJ1c2VyX2lkIjo2fQ.qW6dNm7snKJRSu24DaRFD0XvfvqTiAftNbN8lh1gNNs",
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjkwMjg2MjY0LCJqdGkiOiIwMzE2ODcxMzNkODY0ZmZiODAwMmU2OTNhZGE5MzQ2YiIsInVzZXJfaWQiOjZ9.8Zka41dHa0fCp6GTMNonRN4_sITdgfGqM4oLho9aCdI"
}
```


## 3. Refresh JWT Tokens: POST http://localhost:8000/auth/jwt/refresh

### Description:
This API endpoint allows you to refresh an expired JSON Web Token (JWT) by providing the refresh token.

### Authentication:
Authentication is not required to access this endpoint.

### Request:

#### Method: POST

**Endpoint:** `/auth/jwt/refresh`

**Headers:**
```json
{
    "Content-Type": "application/json"
}
```

**Body:**
```json
{
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY5MDM3MjM2NCwianRpIjoiNTA4ODU4YzRjMGNiNGM0ODlmMTJlZGZjMWFiNjQ2NjQiLCJ1c2VyX2lkIjo2fQ.qW6dNm7snKJRSu24DaRFD0XvfvqTiAftNbN8lh1gNNs"
}
```

### Response:

#### Success Response:
**Code:** 200 OK
**Sample Output:**
```json
{
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjkwMjg2MjY0LCJqdGkiOiIwMzE2ODcxMzNkODY0ZmZiODAwMmU2OTNhZGE5MzQ2YiIsInVzZXJfaWQiOjZ9.8Zka41dHa0fCp6GTMNonRN4_sITdgfGqM4oLho9aCdI"
}
```

## 4. Get Menu Items: GET http://localhost:8000/restaurant/api/items

### Description:
This API endpoint allows you to retrieve a list of restaurant items.

### Authentication:
Authentication is required to access this endpoint.

### Request:

#### Method: GET

**Endpoint:** `/restaurant/api/items`

**Headers:**
```json
{
    "Authorization": "JWT [Your_Access_Token]",
}
```
### Response:

#### Success Response:
**Code:** 200 OK
**Sample Output:**
```json
    [
        {
        "unique_id": 1,
        "name": "Bruschetta",
        "category_name": "Appetizers",
        "category_id": "1",
        "price": "8.99",
        "description": "Toasted bread topped with fresh tomatoes, basil, and garlic."
        },
        {
        "unique_id": 2,
        "name": "Caprese Salad",
        "category_name": "Appetizers",
        "category_id": "1",
        "price": "9.99",
        "description": "Tomatoes, fresh mozzarella, and basil drizzled with balsamic glaze."
        }
    ]
```


## 5. Get Menu Items By Category: GET http://localhost:8000/restaurant/api/items/category/1/

### Description:
This API endpoint allows you to retrieve a list of restaurant items belonging to a specific category.

### Authentication:
Authentication is required to access this endpoint.

### Request:

#### Method: GET

**Endpoint:** `/restaurant/api/items`

**Headers:**
```json
{
    "Authorization": "JWT [Your_Access_Token]",
}
```
### Response:

#### Success Response:
**Code:** 200 OK
**Sample Output:**
```json
    [
        {
        "unique_id": 1,
        "name": "Bruschetta",
        "category_name": "Appetizers",
        "category_id": "1",
        "price": "8.99",
        "description": "Toasted bread topped with fresh tomatoes, basil, and garlic."
        },
        {
        "unique_id": 1,
        "name": "Caprese Salad",
        "category_name": "Appetizers",
        "category_id": "1",
        "price": "9.99",
        "description": "Tomatoes, fresh mozzarella, and basil drizzled with balsamic glaze."
        }
    ]
```


## 6.Search Menu: GET http://localhost:8000/restaurant/api/items/?search=Salad

### Description:
This API endpoint allows you to retrieve a list of restaurant items matching the search query for "Salad".

### Authentication:
Authentication is required to access this endpoint.

### Request:

#### Method: GET

**Endpoint:** `/restaurant/api/items/?search=Salad`

**Headers:**
```json
{
    "Authorization": "JWT [Your_Access_Token]",
}
```
### Response:

#### Success Response:
**Code:** 200 OK
**Sample Output:**
```json
[
    {
        "unique_id": 2,
        "name": "Caprese Salad",
        "category_name": "Appetizers",
        "category_id": "1",
        "price": "9.99",
        "description": "Tomatoes, fresh mozzarella, and basil drizzled with balsamic glaze."
    },
    {
        "unique_id": 4,
        "name": "Greek Salad",
        "category_name": "Salads",
        "category_id": "2",
        "price": "7.99",
        "description": "Crisp lettuce, tomatoes, cucumbers, feta cheese, and olives with Greek dressing."
    }
]
```

## 7. Get Orderst: GET http://localhost:8000/restaurant/api/orders/

### Description:
This API endpoint allows you to retrieve a list of restaurant orders.

### Authentication:
Authentication is required to access this endpoint.

### Request:

#### Method: GET

**Endpoint:** `/restaurant/api/orders/`

**Headers:**
```json
{
    "Authorization": "JWT [Your_Access_Token]",
}
```
### Response:

#### Success Response:
**Code:** 200 OK
**Sample Output:**
```json
    [
        {
            "unique_id": 1,
            "user": "John",
            "status": "PENDING",
            "items": [
                {
                    "name": "Bruschetta",
                    "quantity": 1
                },
                {
                    "name": "Caprese Salad",
                    "quantity": 2
                },
                {
                    "name": "Tiramisu",
                    "quantity": 2
                }
            ],
            "created_at": "2023-07-07T10:00:00Z",
            "updated_at": "2023-07-07T10:15:00Z"
        }
    ]
```


## 8. Create Order: POST http://localhost:8000/restaurant/api/orders/create/

### Description:
This API endpoint allows you to create a new restaurant order.

### Authentication:
Authentication is required to access this endpoint.

### Request:

#### Method: POST

**Endpoint:** `/restaurant/api/orders/create/`

**Headers:**
```json
{
    "Authorization": "JWT [Your_Access_Token]",
}
```

**Body:**
```json
    {
      "user": "Pravallika1",
      "items": [
        {
          "unique_id": 18,
          "quantity": 2
        },
        {
          "unique_id": 15,
          "quantity": 1
        }
      ]
    }
```

### Request Body Parameters:
- `user` (string): The name of the user placing the order.
- `items` (array): An array of objects representing the items and their quantities in the order. Each object should have two properties:
  - `unique_id` (integer): The unique identifier of the item.
  - `quantity` (integer): The quantity of the item to be ordered.

### Response:

#### Success Response:
**Code:** 200 OK
**Sample Output:**
```json
    {
        "order_id": 14,
        "user": "Pravallika1",
        "status": "PENDING",
        "items": [
            {
                "name": "Stuffed Jalapenos",
                "quantity": 2
            },
            {
                "name": "Mojito",
                "quantity": 1
            }
        ]
    }
```


## 9. Update Order: POST http://localhost:8000/restaurant/api/orders/1/items/

### Description:
This API endpoint allows you to add or update items in an existing restaurant order with the specified order ID.

### Authentication:
Authentication is required to access this endpoint.

### Request:

#### Method: POST

**Endpoint:** `/restaurant/api/orders/1/items/`

**Headers:**
```json
{
    "Authorization": "JWT [Your_Access_Token]",
}
```
**Body:**
```json
    {
        "items" : [
            {
                "item" : 12,
                "quantity" : 2
            }
        ]
    }
```

### Request Body Parameters:
- `items` (array): An array of objects representing the items and their quantities to be added or updated in the order. Each object should have two properties:
  - `item` (integer): The unique identifier of the item.
  - `quantity` (integer): The quantity of the item to be added or updated.

### Response:

#### Success Response:
**Code:** 200 OK
**Sample Output:**
```json
    {
        "message": "Items added/updated successfully"
    }
```


## 10. Get Customers: GET http://localhost:8000/restaurant/api/customers

### Description:
This API endpoint allows you to retrieve a list of customers from the restaurant's database.

### Authentication:
Authentication is required to access this endpoint.

### Request:

#### Method: GET

**Endpoint:** `/restaurant/api/customers`

**Headers:**
```json
{
    "Authorization": "JWT [Your_Access_Token]",
}
```
### Response:

#### Success Response:
**Code:** 200 OK
**Sample Output:**
```json
    [
        {
            "id": 1,
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com",
            "phone_number": "1234567890",
            "address": "123 Main Street",
            "date_of_birth": "1990-01-15",
            "created_at": null
        }
    ]
```

## 11. Add New Customer: POST http://localhost:8000/restaurant/api/customers/

### Description:
This API endpoint allows you to create a new customer record in the restaurant's database.

### Authentication:
Authentication is required to access this endpoint.

### Request:

#### Method: POST

**Endpoint:** `/restaurant/api/customers/`

**Headers:**
```json
{
    "Authorization": "JWT [Your_Access_Token]",
}
```
**Body:**
```json
    {
      "first_name": "John",
      "last_name": "Doe",
      "email": "john.doe@example.com",
      "phone_number": "1234567890",
      "address": "123 Main Street",
      "date_of_birth": "1990-01-15"
    }
```

### Request Body Parameters:
- `first_name` (string): The first name of the customer.
- `last_name` (string): The last name of the customer.
- `email` (string): The email address of the customer.
- `phone_number` (string): The phone number of the customer.
- `address` (string): The address of the customer.
- `date_of_birth` (string): The date of birth of the customer in the format "YYYY-MM-DD".

### Response:

#### Success Response:
**Code:** 200 OK
**Sample Output:**

```json
    {
        "id": 6,
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com",
        "phone_number": "1234567890",
        "address": "123 Main Street",
        "date_of_birth": "1990-01-15",
        "created_at": "2023-07-25T12:41:37.033634Z"
    }
```
