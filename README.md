# E-Commerce API

This project is a Flask-based RESTful API for managing an e-commerce system. It provides endpoints to manage customers, products, orders, and customer accounts.

## Features
- **Customer Management:** Add, update, retrieve, and delete customers.
- **Product Management:** Add, update, retrieve, and delete products.
- **Order Management:** Place orders, track orders, and retrieve order details.
- **Customer Account Management:** Add, update, retrieve, and delete customer accounts.

## Technologies Used
- **Python**
- **Flask**
- **Flask SQLAlchemy**
- **Flask Marshmallow**
- **MySQL**

## Installation

### Prerequisites
- Python 3.7+
- MySQL Server
- Virtual environment (optional but recommended)

### Steps
1. Clone the repository:
   ```
   git clone <repository-url>
   cd <repository-folder>
   ```
2. Set up a virtual environment:
   ```
   python3 -m venv venv
   source venv/bin/activate # On Windows use `venv\Scripts\activate`
   ```
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Configure the database connection in the `app.py` file:
   ```
   app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://<username>:<password>@<host>/<database>'
   ```
   Replace `<username>`, `<password>`, `<host>`, and `<database>` with your MySQL credentials.

5. Create the database tables:
   ```
   python app.py
   ```
   The tables will be created when the application starts.

6. Run the application:
   ```
   python app.py
   ```
   The application will run on `http://127.0.0.1:5000/` by default.

## API Endpoints

### Customers
- **GET** `/customers`: Retrieve all customers.
- **POST** `/customers`: Add a new customer.
- **GET** `/customers/<id>`: Retrieve a customer by ID.
- **PUT** `/customers/<id>`: Update a customer by ID.
- **DELETE** `/customers/<id>`: Delete a customer by ID.

### Customer Accounts
- **POST** `/customers/<id>/customer_account`: Add a customer account.
- **GET** `/customers/<id>/customer_account`: Retrieve a customer account.
- **PUT** `/customers/<id>/customer_account`: Update a customer account.
- **DELETE** `/customers/<id>/customer_account`: Delete a customer account.

### Products
- **GET** `/products`: Retrieve all products.
- **POST** `/products`: Add a new product.
- **GET** `/products/<id>`: Retrieve a product by ID.
- **PUT** `/products/<id>`: Update a product by ID.
- **DELETE** `/products/<id>`: Delete a product by ID.

### Orders
- **POST** `/orders`: Place a new order.
- **GET** `/orders/<id>`: Retrieve an order by ID.
- **GET** `/orders/<id>/track`: Track an order by ID.

## Example Usage
To add a new customer, send a POST request to `/customers` with the following JSON payload:
```
{
  "name": "John Doe",
  "email": "john.doe@example.com",
  "phone": "123-456-7890"
}
```

## Dependencies
- **Flask**: Web framework
- **SQLAlchemy**: ORM for database management
- **Marshmallow**: Serialization/deserialization
- **Flask-Bcrypt**: Password hashing
- **MySQL Connector**: MySQL integration



