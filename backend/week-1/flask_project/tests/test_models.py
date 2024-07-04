import pytest
from app import db, create_app
from app.models import Customer, Staff, InventoryItem

@pytest.fixture
def app():
    app = create_app()
    return app

@pytest.fixture
def test_client(app):
    return app.test_client()

@pytest.fixture(scope='function')
def setup_database(app):
    with app.app_context():
        db.create_all()
        yield
        db.session.remove()
        db.drop_all()

def test_customer_model(test_client, setup_database):
    # Create a customer record
    customer = Customer(name='John Doe', email='john@example.com', contact='1234567890')
    
    # Add the customer to the session
    db.session.add(customer)
    db.session.commit()

    # Retrieve the customer from the database
    retrieved_customer = Customer.query.filter_by(email='john@example.com').first()

    # Assert that the retrieved customer matches the created one
    assert retrieved_customer is not None
    assert retrieved_customer.name == 'John Doe'
    assert retrieved_customer.email == 'john@example.com'
    assert retrieved_customer.contact == '1234567890'

def test_staff_model(test_client, setup_database):
    # Create a staff member record
    staff = Staff(name='Jane Smith', email='jane@example.com', contact='1234567890', is_admin=True)

    # Add the staff member to the session
    db.session.add(staff)
    db.session.commit()

    # Retrieve the staff member from the database
    retrieved_staff = Staff.query.filter_by(email='jane@example.com').first()

    # Assert that the retrieved staff member matches the created one
    assert retrieved_staff is not None
    assert retrieved_staff.name == 'Jane Smith'
    assert retrieved_staff.email == 'jane@example.com'
    assert retrieved_staff.contact == '1234567890'
    assert retrieved_staff.is_admin is True

def test_inventory_item_model(test_client, setup_database):
    # Create an inventory item record
    item = InventoryItem(item_sku='SKU123', item_name='Widget', item_price=9.99, item_qty=100)

    # Add the inventory item to the session
    db.session.add(item)
    db.session.commit()

    # Retrieve the inventory item from the database
    retrieved_item = InventoryItem.query.filter_by(item_sku='SKU123').first()

    # Assert that the retrieved inventory item matches the created one
    assert retrieved_item is not None
    assert retrieved_item.item_name == 'Widget'
    assert retrieved_item.item_price == 9.99
    assert retrieved_item.item_qty == 100
