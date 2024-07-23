from flask import Blueprint, request, jsonify , abort
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from app.models import Customer, InventoryItem
import logging
import requests

bp = Blueprint('routes', __name__)
bp = Blueprint('auth', __name__)
CORS(bp)

# Configure logging
logging.basicConfig(level=logging.DEBUG)

@bp.route('/api/signup', methods=['POST'])
def signup():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No input data provided'}), 400

    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not username or not email or not password:
        return jsonify({'error': 'Missing required parameters'}), 400

    try:
        new_customer = Customer(username=username, email=email)
        new_customer.password = password  # Set the password using the property
        db.session.add(new_customer)
        db.session.commit()
        return jsonify({'message': 'Account created successfully'}), 201
    except Exception as e:
        db.session.rollback()
        logging.error(f"Error creating customer: {e}")
        return jsonify({'error': str(e)}), 500


@bp.route('/api/login/', methods=['POST'])
def login():
    data = request.get_json()
    if not data:
        logging.debug("No input data provided")
        return jsonify({"message": "No input data provided"}), 400

    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        logging.debug("Missing username or password")
        return jsonify({"message": "Missing username or password!"}), 400

    try:
        customer = Customer.query.filter_by(username=username).first()
        if customer:
            logging.debug(f"Customer found: {customer.username}")
            if customer.check_password(password):
                # Generate a token here if needed
                token = "redirecting to dashboard"  # Replace with actual token generation
                logging.debug("Login successful, token generated")
                return jsonify({"message": "Login successful!", "token": token}), 200
            else:
                logging.debug("Invalid password")
                return jsonify({"message": "Invalid credentials!"}), 401
        else:
            logging.debug("Customer not found")
            return jsonify({"message": "Invalid credentials!"}), 401

    except Exception as e:
        logging.error(f"Error during login: {e}")
        return jsonify({"message": "Server error. Please try again later."}), 500


@bp.route('/api/products', methods=['GET', 'POST'])
def manage_products():
    if request.method == 'POST':
        data = request.get_json()

        if not data or not all(k in data for k in ('name', 'quantity', 'price')):
            return jsonify({'error': 'Missing required parameters'}), 400

        new_product = InventoryItem(
            name=data['name'],
            description=data.get('description'),
            quantity=data['quantity'],
            price=data['price']
        )
        try:
            db.session.add(new_product)
            db.session.commit()
            return jsonify({"message": "Product created successfully!"}), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500

    elif request.method == 'GET':
        products = InventoryItem.query.all()
        return jsonify([{
            'id': product.id,
            'name': product.name,
            'description': product.description,
            'quantity': product.quantity,
            'price': product.price
        } for product in products]), 200

@bp.route('/api/products/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def manage_product(id):
    product = InventoryItem.query.get_or_404(id)

    if request.method == 'GET':
        return jsonify({
            'id': product.id,
            'name': product.name,
            'description': product.description,
            'quantity': product.quantity,
            'price': product.price
        }), 200

    elif request.method == 'PUT':
        data = request.get_json()

        if not data or not all(k in data for k in ('name', 'quantity', 'price')):
            return jsonify({'error': 'Missing required parameters'}), 400

        product.name = data['name']
        product.description = data.get('description')
        product.quantity = data['quantity']
        product.price = data['price']
        try:
            db.session.commit()
            return jsonify({"message": "Product updated successfully!"}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500

    elif request.method == 'DELETE':
        try:
            db.session.delete(product)
            db.session.commit()
            return jsonify({"message": "Product deleted successfully!"}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500

    else:
        abort(405)  # Method Not Allowed
