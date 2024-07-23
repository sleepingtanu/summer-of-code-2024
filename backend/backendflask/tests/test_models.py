import pytest
from app import create_app, db
from app.models import Customer, Staff, InventoryItem, Transaction

@pytest.fixture(scope='module')
def test_client():
    flask_app = create_app()
    flask_app.config['TESTING'] = True
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres25:tanvi12345@localhost:5432/pos_db'
    
    testing_client = flask_app.test_client()
    
    with flask_app.app_context():
        db.create_all()
        yield testing_client
        db.drop_all()

@pytest.fixture(scope='function')
def new_customer():
    customer = Customer(name='John Doe', email='john@example.com', contact='1234567890')
    db.session.add(customer)
    db.session.commit()
    return customer

@pytest.fixture(scope='function')
def new_staff():
    staff = Staff(name='Jane Smith', email='jane@example.com', role='Manager')
    db.session.add(staff)
    db.session.commit()
    return staff

@pytest.fixture(scope='function')
def new_inventory_item():
    item = InventoryItem(name='Laptop', description='A powerful laptop', quantity=10, price=999.99)
    db.session.add(item)
    db.session.commit()
    return item

@pytest.fixture(scope='function')
def new_transaction(new_customer, new_staff, new_inventory_item):
    transaction = Transaction(customer_id=new_customer.id, staff_id=new_staff.id, inventory_item_id=new_inventory_item.id, quantity=1)
    db.session.add(transaction)
    db.session.commit()
    return transaction

def test_customer_model(test_client):
    customer = Customer(name='John Doe', email='john@example.com', contact='1234567890')
    db.session.add(customer)
    db.session.commit()

    assert customer.id is not None
    assert customer.name == 'John Doe'
    assert customer.email == 'john@example.com'
    assert customer.contact == '1234567890'

def test_staff_model(test_client):
    staff = Staff(name='Jane Smith', email='jane@example.com', role='Manager')
    db.session.add(staff)
    db.session.commit()

    assert staff.id is not None
    assert staff.name == 'Jane Smith'
    assert staff.email == 'jane@example.com'
    assert staff.role == 'Manager'

def test_inventory_item_model(test_client):
    item = InventoryItem(name='Laptop', description='A powerful laptop', quantity=10, price=999.99)
    db.session.add(item)
    db.session.commit()

    assert item.id is not None
    assert item.name == 'Laptop'
    assert item.description == 'A powerful laptop'
    assert item.quantity == 10
    assert item.price == 999.99

def test_transaction_model(test_client, new_customer, new_staff, new_inventory_item):
    transaction = Transaction(customer_id=new_customer.id, staff_id=new_staff.id, inventory_item_id=new_inventory_item.id, quantity=1)
    db.session.add(transaction)
    db.session.commit()

    assert transaction.id is not None
    assert transaction.customer_id == new_customer.id
    assert transaction.staff_id == new_staff.id
    assert transaction.inventory_item_id == new_inventory_item.id
    assert transaction.quantity == 1
