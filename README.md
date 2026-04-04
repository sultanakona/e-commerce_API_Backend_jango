# E-commerce API Backend

## Introduction
This is the backend of an e-commerce API built using Django. It provides various endpoints that allow the management of products, orders, users, and other related entities in an e-commerce platform.

## Dependencies
- Django >= 3.2
- Django REST Framework >= 3.12
- PostgreSQL >= 13
- djangorestframework-jwt
- psycopg2-binary

## Project Structure
```
├── e_commerce_api_backend  # Project folder
│   ├── settings.py          # Configuration settings
│   ├── urls.py              # URL routing
│   ├── wsgi.py              # WSGI application
│   ├── apps                 # Apps folder
│   │   ├── products         # Products app
│   │   ├── users            # Users app
│   │   └── orders           # Orders app
│   └── manage.py            # Command line utility
└── requirements.txt          # Project dependencies
```

## API Endpoints
### Authentication
- **POST /api/auth/login/**  
  Logs a user in and returns an access token.

### Product Management
- **GET /api/products/**  
  Returns a list of products.
- **POST /api/products/**  
  Creates a new product.

### Order Management
- **GET /api/orders/**  
  Returns a list of orders.
- **POST /api/orders/**  
  Creates a new order.

## Database Setup
1. Install PostgreSQL on your machine.
2. Create a database for the project. 
   ```sql
   CREATE DATABASE e_commerce_db;
   ```
3. Update the `DATABASES` setting in `settings.py` with your database credentials.

## Installation Instructions
1. Clone the repository:
   ```bash
   git clone https://github.com/sultanakona/e-commerce_API_Backend_jango.git
   ```
2. Navigate to the project directory:
   ```bash
   cd e-commerce_API_Backend_jango
   ```
3. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the migrations:
   ```bash
   python manage.py migrate
   ```
5. Start the development server:
   ```bash
   python manage.py runserver
   ```

## Configuration
- Update the `settings.py` file with your environment-specific configurations like DEBUG, ALLOWED_HOSTS, and database settings.

## Usage Examples
### Logging In
```bash
curl -X POST http://localhost:8000/api/auth/login/ -d '{"username":"your_username", "password":"your_password"}' -H 'Content-Type: application/json'
```

### Getting Products
```bash
curl -X GET http://localhost:8000/api/products/
```

### Creating an Order
```bash
curl -X POST http://localhost:8000/api/orders/ -d '{"product_id": 1, "quantity": 2}' -H 'Content-Type: application/json' -H 'Authorization: Bearer <your_token>'
```

## Conclusion
This e-commerce API backend is designed to be easy to use and scalable for various e-commerce applications. Feel free to contribute or improve this project.