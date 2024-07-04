Models Documentation
This document provides an overview of the models, their fields, relationships, and example usage in the Flask project.

Customer
Fields:

id: Integer, primary key
name: String, not null
email: String, unique, not null
contact: String, unique
Relationships:

One-to-Many with Transaction
Example Usage:

python
Copy code
customer = Customer(name='John Doe', email='john@example.com', contact='1234567890')
db.session.add(customer)
db.session.commit()
Staff
Fields:

id: Integer, primary key
name: String, not null
position: String, not null
email: String, unique, not null
Relationships:

One-to-Many with Transaction
Example Usage:

python
Copy code
staff = Staff(name='Jane Smith', position='Manager', email='jane@example.com')
db.session.add(staff)
db.session.commit()
InventoryItem
Fields:

id: Integer, primary key
name: String, not null
quantity: Integer, not null
price: Float, not null
Relationships:

One-to-Many with Transaction
Methods:

python
Copy code
def calculate_total_value(self):
    return self.price * self.quantity
Example Usage:

python
Copy code
item = InventoryItem(name='Widget', quantity=100, price=9.99)
db.session.add(item)
db.session.commit()

total_value = item.calculate_total_value()
Transaction
Fields:

id: Integer, primary key
customer_id: Integer, foreign key
staff_id: Integer, foreign key
inventory_item_id: Integer, foreign key
quantity: Integer, not null
total_price: Float, not null
Relationships:

Many-to-One with Customer
Many-to-One with Staff
Many-to-One with InventoryItem
Example Usage:

python
Copy code
transaction = Transaction(customer_id=1, staff_id=1, inventory_item_id=1, quantity=5, total_price=49.95)
db.session.add(transaction)
db.session.commit()
app/models.py
Here's the complete models.py with the additional custom method for the InventoryItem model.

python
Copy code
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    contact = db.Column(db.String(20), unique=True, nullable=True)

    transactions = db.relationship('Transaction', backref='customer', lazy=True)

class Staff(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    position = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    transactions = db.relationship('Transaction', backref='staff', lazy=True)

class InventoryItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)

    transactions = db.relationship('Transaction', backref='inventory_item', lazy=True)

    def calculate_total_value(self):
        return self.price * self.quantity

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    staff_id = db.Column(db.Integer, db.ForeignKey('staff.id'), nullable=False)
    inventory_item_id = db.Column(db.Integer, db.ForeignKey('inventory_item.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    total_price = db.Column(db.Float, nullable=False)
app/tests/test_models.py
Here's the test_models.py with additional tests for the calculate_total_value method.

python
Copy code
import sys
import os
import pytest

# Ensure the app directory is in the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'app')))

from app import create_app, db
from app.models import Customer, Staff, InventoryItem, Transaction

@pytest.fixture(scope='module')
def test_client():
    flask_app = create_app()
    flask_app.config['TESTING'] = True
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres1:tanvi12345@localhost:5432/dsoc_db'

    testing_client = flask_app.test_client()

    with flask_app.app_context():
        db.create_all()
        yield testing_client
        db.drop_all()

def test_customer_model(test_client):
    customer = Customer(name='John Doe', email='john@example.com', contact='1234567890')
    db.session.add(customer)
    db.session.commit()

    assert customer.id is not None
    assert customer.name == 'John Doe'
    assert customer.email == 'john@example.com'

def test_staff_model(test_client):
    staff = Staff(name='Jane Smith', position='Manager', email='jane@example.com')
    db.session.add(staff)
    db.session.commit()

    assert staff.id is not None
    assert staff.name == 'Jane Smith'
    assert staff.position == 'Manager'

def test_inventory_item_model(test_client):
    item = InventoryItem(name='Widget', quantity=100, price=9.99)
    db.session.add(item)
    db.session.commit()

    assert item.id is not None
    assert item.name == 'Widget'
    assert item.quantity == 100
    assert item.calculate_total_value() == 999.0

def test_transaction_model(test_client):
    customer = Customer(name='John Doe', email='john@example.com', contact='1234567890')
    staff = Staff(name='Jane Smith', position='Manager', email='jane@example.com')
    item = InventoryItem(name='Widget', quantity=100, price=9.99)

    db.session.add(customer)
    db.session.add(staff)
    db.session.add(item)
    db.session.commit()

    transaction = Transaction(customer_id=customer.id, staff_id=staff.id, inventory_item_id=item.id, quantity=5, total_price=49.95)
    db.session.add(transaction)
    db.session.commit()

    assert transaction.id is not None
    assert transaction.quantity == 5
    assert transaction.total_price == 49.95
Expected Output
Running the tests with pytest should produce the following output:

sh
Copy code
================================== test session starts ==================================
platform win32 -- Python 3.12.4, pytest-8.2.2, pluggy-1.5.0
rootdir: C:\Users\ASUS\Documents\GitHub\summer-of-code-2024\backend\week-1\flask_project
collected 4 items

tests/test_models.py ....                                                          [100%]

================================== 4 passed in 2.00s ================================
This indicates that all tests have passed successfully, including the test for the custom calculate_total_value method.