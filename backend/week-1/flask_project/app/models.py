from app import db
from sqlalchemy.orm import validates

class InventoryItem(db.Model):
    __tablename__ = 'inventory_items'
    id = db.Column(db.Integer, primary_key=True)
    item_sku = db.Column(db.String(50), unique=True, nullable=False)
    item_name = db.Column(db.String(100), nullable=False)
    item_description = db.Column(db.String(200))
    item_price = db.Column(db.Float, nullable=False)
    item_qty = db.Column(db.Integer, nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey('inventory_items.id'))
    children = db.relationship('InventoryItem', remote_side=[id])

class Customer(db.Model):
    __tablename__ = 'customers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    contact = db.Column(db.String(20))

    @validates('email')
    def validate_email(self, key, address):
        assert '@' in address
        return address

class Staff(db.Model):
    __tablename__ = 'staff'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    contact = db.Column(db.String(20))

class Transaction(db.Model):
    __tablename__ = 'transactions'
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    staff_id = db.Column(db.Integer, db.ForeignKey('staff.id'), nullable=False)
    inventory_item_id = db.Column(db.Integer, db.ForeignKey('inventory_items.id'), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    amount = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50))

    customer = db.relationship('Customer', backref=db.backref('transactions', lazy=True))
    staff = db.relationship('Staff', backref=db.backref('transactions', lazy=True))
    inventory_item = db.relationship('InventoryItem', backref=db.backref('transactions', lazy=True))
