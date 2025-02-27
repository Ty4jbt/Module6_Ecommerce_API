
from datetime import timedelta
from sqlalchemy.dialects.mysql import JSON
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from marshmallow import fields, ValidationError
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from flask_bcrypt import Bcrypt
from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:Full-Stack-dev97@localhost/e_commerce_db'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
ma = Marshmallow(app)
CORS(app)

class CustomerSchema(ma.SQLAlchemyAutoSchema):
    name = fields.String(required=True)
    email = fields.String(required=True)
    phone = fields.String(required=True)

    class Meta:
        fields = ('name', 'email', 'phone', 'id')

customer_schema = CustomerSchema()
customers_schema = CustomerSchema(many=True)

class ProductSchema(ma.SQLAlchemyAutoSchema):
    name = fields.String(required=True)
    price = fields.Float(required=True)

    class Meta:
        fields = ('name', 'price', 'id')

product_schema = ProductSchema()
products_schema = ProductSchema(many=True)

class Customer(db.Model):
    __tablename__ = 'Customers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(320))
    phone = db.Column(db.String(15))
    orders = db.relationship('Order', backref='customer', lazy='dynamic')

class Order(db.Model):
    __tablename__ = 'Orders'
    id = db.Column(db.Integer, primary_key=True)
    order_date = db.Column(db.DateTime, nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('Customers.id'), nullable=False)
    product_list = db.Column(JSON)

order_product = db.Table('Order_Product',
    db.Column('order_id', db.Integer, db.ForeignKey('Orders.id'), primary_key=True),
    db.Column('product_id', db.Integer, db.ForeignKey('Products.id'), primary_key=True)
)

class Product(db.Model):
    __tablename__ = 'Products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Float, nullable=False)
    orders = db.relationship('Order', secondary=order_product, backref=db.backref('products'))

class Customer_Account(db.Model):
    __tablename__ = 'Customer_Accounts'
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('Customers.id'))
    username = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

@app.route('/customers', methods=['GET'])
def get_customers():
    customers = Customer.query.all()
    return customers_schema.jsonify(customers)

@app.route('/customers', methods=['POST'])
def add_customer():
    try:
        customer_data = customer_schema.load(request.json)

    except ValidationError as err:
        return jsonify(err.messages), 400
    
    new_customer = Customer(name=customer_data['name'], email=customer_data['email'], phone=customer_data['phone'])

    db.session.add(new_customer)
    db.session.commit()

    return jsonify({'message': 'New customer added successfully.'}), 201

@app.route('/customers/<int:id>', methods=['PUT'])
def update_customer(id):
    customer = Customer.query.get_or_404(id)

    try:
        customer_data = customer_schema.load(request.json)

    except ValidationError as err:
        return jsonify(err.messages), 400

    customer.name = customer_data['name']
    customer.email = customer_data['email']
    customer.phone = customer_data['phone']

    db.session.commit()

    return jsonify({'message': 'Customer updated successfully.'}), 200

@app.route('/customers/<int:id>', methods=['DELETE'])
def delete_customer(id):
    customer = Customer.query.get_or_404(id)

    # Delete associated customer account
    Customer_Account.query.filter_by(customer_id=id).delete()
    
    # Delete associated orders
    Order.query.filter_by(customer_id=id).delete()

    db.session.delete(customer)
    db.session.commit()

    return jsonify({'message': 'Customer deleted successfully.'}), 200

@app.route('/customers/<int:id>', methods=['GET'])
def get_customer_by_id(id):
    customer = Customer.query.get_or_404(id)
    return customer_schema.jsonify(customer)

@app.route('/customers/<int:id>/customer_account', methods=['POST'])
def add_customer_account(id):
    customer = Customer.query.get_or_404(id)
    customer_account_data = request.json

    new_customer_account = Customer_Account(customer_id=customer.id, username=customer_account_data['username'], password=bcrypt.generate_password_hash(customer_account_data['password']).decode('utf-8'))

    db.session.add(new_customer_account)
    db.session.commit()

    return jsonify({'message': 'New customer account added successfully.'}), 201

@app.route('/customers/<int:id>/customer_account', methods=['GET'])
def get_customer_account(id):
    customer = Customer.query.get_or_404(id)
    customer_account = Customer_Account.query.filter_by(customer_id=customer.id).first()

    return jsonify({'username': customer_account.username})

@app.route('/customers/<int:id>/customer_account', methods=['PUT'])
def update_customer_account(id):
    customer = Customer.query.get_or_404(id)
    customer_account = Customer_Account.query.filter_by(customer_id=customer.id).first()
    customer_account_data = request.json

    customer_account.username = customer_account_data['username']
    customer_account.password = bcrypt.generate_password_hash(customer_account_data['password']).decode('utf-8')

    db.session.commit()

    return jsonify({'message': 'Customer account updated successfully.'}), 200

@app.route('/customers/<int:id>/customer_account', methods=['DELETE'])
def delete_customer_account(id):
    customer = Customer.query.get_or_404(id)
    customer_account = Customer_Account.query.filter_by(customer_id=customer.id).first()

    db.session.delete(customer_account)
    db.session.commit()

    return jsonify({'message': 'Customer account deleted successfully.'}), 200

@app.route('/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    return products_schema.jsonify(products)

@app.route('/products', methods=['POST'])
def add_product():
    product_data = request.json

    new_product = Product(name=product_data['name'], price=product_data['price'])

    db.session.add(new_product)
    db.session.commit()

    return jsonify({'message': 'New product added successfully.'}), 201

@app.route('/products/<int:id>', methods=['PUT'])
def update_product(id):
    product = Product.query.get_or_404(id)
    product_data = request.json

    product.name = product_data['name']
    product.price = product_data['price']

    db.session.commit()

    return jsonify({'message': 'Product updated successfully.'}), 200

@app.route('/products/<int:id>', methods=['DELETE'])
def delete_product(id):
    product = Product.query.get_or_404(id)

    db.session.delete(product)
    db.session.commit()

    return jsonify({'message': 'Product deleted successfully.'}), 200

@app.route('/products/<int:id>', methods=['GET'])
def get_product_by_id(id):
    product = Product.query.get_or_404(id)
    return product_schema.jsonify(product)

@app.route('/orders', methods=['POST'])
def add_order():
    order_data = request.json
    product_list = []

    for product_item in order_data['products']:
        product_id = product_item['product_id']
        product = Product.query.get_or_404(product_id)
        
        product_list.append({
            'id': product.id,
            'name': product.name,
            'price': product.price,
            'quantity': product_item['quantity']
        })

    new_order = Order(
        order_date=order_data['orderDate'],
        customer_id=order_data['customerId'],
        product_list=product_list
    )

    db.session.add(new_order)
    db.session.commit()

    return jsonify({'message': 'New order added successfully.'}), 201

@app.route('/orders/<int:id>', methods=['GET'])
def get_order_by_id(id):
    order = Order.query.get_or_404(id)
    return jsonify({'order_date': order.order_date, 'customer': order.customer.name, 'products': [product.name for product in order.products]})

@app.route('/orders/<int:id>/track', methods=['GET'])
def track_order(id):
    order = Order.query.get_or_404(id)
    expected_delivery_date = order.order_date + timedelta(days=7)  # Assuming delivery takes 7 days
    return jsonify({
        'order_date': order.order_date,
        'expected_delivery_date': expected_delivery_date
    })

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)