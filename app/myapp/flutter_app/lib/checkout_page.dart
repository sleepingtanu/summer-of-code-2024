// ignore_for_file: library_private_types_in_public_api

import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';
import 'services/firestore_service.dart';
import 'product_model.dart';

class CheckoutPage extends StatefulWidget {
  const CheckoutPage({super.key});

  @override
  _CheckoutPageState createState() => _CheckoutPageState();
}

class _CheckoutPageState extends State<CheckoutPage> {
  final FirestoreService _firestoreService = FirestoreService();
  final TextEditingController _barcodeController = TextEditingController();
  String? _productInfo;

  Future<void> _fetchProduct() async {
    String barcode = _barcodeController.text;
    if (kDebugMode) {
      print('Fetching product with barcode: $barcode');
    }

    // Fetch the product from Firestore using the barcode
    Product? product = await _firestoreService.getProduct('barcode: $barcode');

    if (kDebugMode) {
      print('Product fetched: $product');
    }

    // Check if product is null
    // ignore: unnecessary_null_comparison
    if (product == null) {
      setState(() {
        _productInfo = 'Product not found';
      });
      return;
    }

    // Extract product details
    String name = product.name;
    double price = product.price;

    // Update the UI with the fetched product information
    setState(() {
      _productInfo = 'Name: $name, Price: $price';
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Checkout'),
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          children: [
            TextField(
              controller: _barcodeController,
              decoration: const InputDecoration(labelText: 'Barcode Number'),
            ),
            ElevatedButton(
              onPressed: _fetchProduct,
              child: const Text('Fetch Product'),
            ),
            _productInfo != null ? Text(_productInfo!) : Container(),
          ],
        ),
      ),
    );
  }
}
