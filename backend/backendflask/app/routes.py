from flask import Blueprint, app, redirect, render_template, request, jsonify , abort, url_for
from flask_cors import CORS
from flask_login import current_user, login_required, logout_user
from flask_mail import Message
from itsdangerous import BadTimeSignature, SignatureExpired
import pyotp
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from app.models import Customer, InventoryItem, Staff, Transaction
import logging
import requests
import pandas as pd
from matplotlib import pyplot as plt

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
@app.route('/api/logout')
@login_required
def api_logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/confirm_email/<token>')
def confirm_email(token):
    try:
        email = s.loads(token, salt='email-confirm', max_age=3600) # type: ignore
        staff = Staff.query.filter_by(email=email).first()
        if staff:
            staff.is_approved = True
            db.session.commit()
            return jsonify({'message': 'Email confirmed! You can now log in.'}), 200
        else:
            return jsonify({'message': 'Invalid token!'}), 400
    except SignatureExpired:
        return jsonify({'message': 'The token is expired!'}), 400
    except BadTimeSignature:
        return jsonify({'message': 'Invalid token!'}), 400
    
@app.route('/api/forgot_password', methods=['POST'])
def forgot_password():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No input data provided'}), 400

    email = data.get('email')
    staff = Staff.query.filter_by(email=email).first()
    if not staff:
        return jsonify({'error': 'No account with that email address'}), 400

    token = s.dumps(email, salt='password-reset') # type: ignore
    msg = Message('Password Reset Request', sender='noreply@yourapp.com', recipients=[email])
    link = url_for('reset_password', token=token, _external=True)
    msg.body = f'Your link is {link}'
    email.send(msg)
    return jsonify({'message': 'Password reset link sent to your email'}), 200

@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    try:
        email = s.loads(token, salt='password-reset', max_age=3600) # type: ignore
    except SignatureExpired:
        return jsonify({'message': 'The token is expired!'}), 400
    except BadTimeSignature:
        return jsonify({'message': 'Invalid token!'}), 400

    if request.method == 'POST':
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No input data provided'}), 400

        password = data.get('password')
        if not password:
            return jsonify({'error': 'Password is required'}), 400

        staff = Staff.query.filter_by(email=email).first()
        staff.set_password(password)
        db.session.commit()
        return jsonify({'message': 'Password has been reset successfully'}), 200

    return render_template('reset_password.html', token=token)


@app.route('/api/setup_mfa', methods=['GET'])
@login_required
def setup_mfa():
    secret = current_user.get_mfa_secret()
    otp_url = pyotp.totp.TOTP(secret).provisioning_uri(current_user.email, issuer_name="YourAppName")
    return jsonify({'otp_url': otp_url})

@app.route('/api/verify_mfa', methods=['POST'])
@login_required
def verify_mfa():
    data = request.get_json()
    token = data.get('token')
    if not token:
        return jsonify({'error': 'Token is required'}), 400

    totp = pyotp.TOTP(current_user.get_mfa_secret())
    if totp.verify(token):
        return jsonify({'message': 'MFA verified successfully'}), 200
    else:
        return jsonify({'error': 'Invalid token'}), 400

@app.route('/api/staff', methods=['POST'])
@login_required
def create_staff():
    if not current_user.is_admin:
        return jsonify({'error': 'Unauthorized access'}), 403

    data = request.get_json()
    if not data:
        return jsonify({'error': 'No input data provided'}), 400

    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    is_admin = data.get('is_admin', False)

    if not username or not email or not password:
        return jsonify({'error': 'Missing required parameters'}), 400

    try:
        new_staff = Staff(username=username, email=email, is_admin=is_admin)
        new_staff.set_password(password)
        db.session.add(new_staff)
        db.session.commit()
        return jsonify({'message': 'Staff created successfully'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/staff/<int:id>', methods=['PUT'])
@login_required
def update_staff(id):
    if not current_user.is_admin:
        return jsonify({'error': 'Unauthorized access'}), 403

    data = request.get_json()
    staff = Staff.query.get_or_404(id)

    staff.username = data.get('username', staff.username)
    staff.email = data.get('email', staff.email)
    if data.get('password'):
        staff.set_password(data['password'])
    staff.is_admin = data.get('is_admin', staff.is_admin)
    staff.is_approved = data.get('is_approved', staff.is_approved)

    try:
        db.session.commit()
        return jsonify({'message': 'Staff updated successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/staff/<int:id>', methods=['DELETE'])
@login_required
def delete_staff(id):
    if not current_user.is_admin:
        return jsonify({'error': 'Unauthorized access'}), 403

    staff = Staff.query.get_or_404(id)
    try:
        db.session.delete(staff)
        db.session.commit()
        return jsonify({'message': 'Staff deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/staff', methods=['GET'])
@login_required
def get_staff():
    if not current_user.is_admin:
        return jsonify({'error': 'Unauthorized access'}), 403

    staff = Staff.query.all()
    return jsonify([s.to_dict() for s in staff]), 200

@app.route('/api/customers', methods=['POST'])
@login_required
def create_customer():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No input data provided'}), 400

    username = data.get('username')
    email = data.get('email')

    if not username or not email:
        return jsonify({'error': 'Missing required parameters'}), 400

    try:
        new_customer = Customer(username=username, email=email)
        db.session.add(new_customer)
        db.session.commit()
        return jsonify({'message': 'Customer created successfully'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/customers/<int:id>', methods=['PUT'])
@login_required
def update_customer(id):
    data = request.get_json()
    customer = Customer.query.get_or_404(id)

    customer.username = data.get('username', customer.username)
    customer.email = data.get('email', customer.email)

    try:
        db.session.commit()
        return jsonify({'message': 'Customer updated successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/customers/<int:id>', methods=['DELETE'])
@login_required
def delete_customer(id):
    customer = Customer.query.get_or_404(id)
    try:
        db.session.delete(customer)
        db.session.commit()
        return jsonify({'message': 'Customer deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/customers', methods=['GET'])
@login_required
def get_customers():
    customers = Customer.query.all()
    return jsonify([customer.to_dict() for customer in customers]), 200

@app.route('/api/transactions', methods=['POST'])
@login_required
def create_transaction():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No input data provided'}), 400

    c_id = data.get('c_id')
    s_id = data.get('s_id')
    product_amount_list = data.get('product_amount_list')
    date = data.get('date')
    time = data.get('time')

    if not c_id or not s_id or not product_amount_list or not date or not time:
        return jsonify({'error': 'Missing required parameters'}), 400

    try:
        new_transaction = Transaction(c_id=c_id, s_id=s_id, product_amount_list=product_amount_list, date=date, time=time)
        db.session.add(new_transaction)
        db.session.commit()
        return jsonify({'message': 'Transaction created successfully'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/transactions', methods=['GET'])
@login_required
def get_transactions():
    transactions = Transaction.query.all()
    return jsonify([transaction.to_dict() for transaction in transactions]), 200

@app.route('/api/transactions/<int:id>', methods=['GET'])
@login_required
def get_transaction_by_id(id):
    transaction = Transaction.query.get_or_404(id)
    return jsonify(transaction.to_dict()), 200

@app.route('/api/transactions/<int:id>', methods=['PUT'])
@login_required
def update_transaction(id):
    data = request.get_json()
    transaction = Transaction.query.get_or_404(id)

    transaction.c_id = data.get('c_id', transaction.c_id)
    transaction.s_id = data.get('s_id', transaction.s_id)
    transaction.product_amount_list = data.get('product_amount_list', transaction.product_amount_list)
    transaction.date = data.get('date', transaction.date)
    transaction.time = data.get('time', transaction.time)

    try:
        db.session.commit()
        return jsonify({'message': 'Transaction updated successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/transactions/<int:id>', methods=['DELETE'])
@login_required
def delete_transaction(id):
    transaction = Transaction.query.get_or_404(id)
    try:
        db.session.delete(transaction)
        db.session.commit()
        return jsonify({'message': 'Transaction deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
    

@app.route('/api/transaction_analytics', methods=['GET'])
@login_required
def transaction_analytics():
    transactions = Transaction.query.all()
    df = pd.DataFrame([transaction.to_dict() for transaction in transactions])
    # Perform analytics
    sales_by_date = df.groupby('date')['product_amount_list'].sum()
    sales_by_date.plot(kind='bar')
    plt.xlabel('Date')
    plt.ylabel('Sales')
    plt.title('Sales by Date')
    plt.savefig('sales_by_date.png')
    return jsonify({'message': 'Analytics generated successfully'}), 200


