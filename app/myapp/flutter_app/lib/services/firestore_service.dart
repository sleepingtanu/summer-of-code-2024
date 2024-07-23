import 'package:cloud_firestore/cloud_firestore.dart' as firestore;
import 'package:flutter_app/transaction_model.dart' as models;
import 'package:cloud_firestore/cloud_firestore.dart';
import 'package:flutter_app/customer_model.dart';
import 'package:flutter_app/product_model.dart';

class FirestoreService {
  final firestore.FirebaseFirestore _db = firestore.FirebaseFirestore.instance;

  // Add a customer
  Future<void> addCustomer(Customer customer) {
    return _db.collection('customers').doc(customer.id).set(customer.toMap());
  }

  // Get a customer by ID
  Future<Customer> getCustomer(String id) async {
    DocumentSnapshot doc = await _db.collection('customers').doc(id).get();
    if (doc.exists) {
      return Customer.fromMap(doc.data() as Map<String, dynamic>);
    } else {
      throw Exception('Customer not found');
    }
  }

  // Update a customer
  Future<void> updateCustomer(Customer customer) {
    return _db
        .collection('customers')
        .doc(customer.id)
        .update(customer.toMap());
  }

  // Delete a customer
  Future<void> deleteCustomer(String id) {
    return _db.collection('customers').doc(id).delete();
  }

  // Add a product
  Future<void> addProduct(Product product) {
    return _db.collection('products').doc(product.id).set(product.toMap());
  }

  // Get a product by ID
  Future<Product> getProduct(String id) async {
    DocumentSnapshot doc = await _db.collection('products').doc(id).get();
    if (doc.exists) {
      return Product.fromMap(doc.data() as Map<String, dynamic>);
    } else {
      throw Exception('Product not found');
    }
  }

  // Update a product
  Future<void> updateProduct(Product product) {
    return _db.collection('products').doc(product.id).update(product.toMap());
  }

  // Delete a product
  Future<void> deleteProduct(String id) {
    return _db.collection('products').doc(id).delete();
  }

  // Add a transaction
  Future<void> addTransaction(models.Transaction transaction) {
    return _db
        .collection('transactions')
        .doc(transaction.id)
        .set(transaction.toMap());
  }

  // Get a transaction by ID
  Future<models.Transaction> getTransaction(String id) async {
    firestore.DocumentSnapshot doc = await _db.collection('transactions').doc(id).get();
    if (doc.exists) {
      return models.Transaction.fromMap(doc.data() as Map<String, dynamic>);
    } else {
      throw Exception('Transaction not found');
    }
  }

  // Update a transaction
  Future<void> updateTransaction(models.Transaction transaction) {
    return _db
        .collection('transactions')
        .doc(transaction.id)
        .update(transaction.toMap());
  }

  // Delete a transaction
  Future<void> deleteTransaction(String id) {
    return _db.collection('transactions').doc(id).delete();
  }

}

