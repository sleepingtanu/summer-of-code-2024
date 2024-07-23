class Product {
  String id;
  String name;
  double price;
  String barcode;
  String imageUrl;

  Product(
      {required this.id,
      required this.name,
      required this.price,
      required this.barcode,
      required this.imageUrl});

  Map<String, dynamic> toMap() {
    return {
      'id': id,
      'name': name,
      'price': price,
      'barcode': barcode,
      'imageUrl': imageUrl,
    };
  }

  static Product fromMap(Map<String, dynamic> map) {
    return Product(
      id: map['id'],
      name: map['name'],
      price: map['price'],
      barcode: map['barcode'],
      imageUrl: map['imageUrl'],
    );
  }
}
