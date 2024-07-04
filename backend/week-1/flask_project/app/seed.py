from app import db
from app.models import InventoryItem, Customer, Staff, Transaction
from datetime import datetime

def seed_data():
    item1 = InventoryItem(item_sku='SKU001', item_name='Item 1', item_description='Description 1', item_price=10.0, item_qty=100)
    customer1 = Customer(name='Alice', email='alice@example.com', contact='1111111111')
    staff1 = Staff(name='Bob', email='bob@example.com', is_admin=True, contact='2222222222')
    transaction1 = Transaction(customer_id=1, staff_id=1, inventory_item_id=1, date=datetime.now(), amount=50.0, category='Category 1')

    db.session.add(item1)
    db.session.add(customer1)
    db.session.add(staff1)
    db.session.add(transaction1)
    db.session.commit()

if __name__ == '__main__':
    seed_data()
