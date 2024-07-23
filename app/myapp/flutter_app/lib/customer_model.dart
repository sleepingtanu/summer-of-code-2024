class Customer {
  String id;
  String name;
  String email;
  String phone;

  Customer(
      {required this.id,
      required this.name,
      required this.email,
      required this.phone});

  Map<String, dynamic> toMap() {
    return {
      'id': id,
      'name': name,
      'email': email,
      'phone': phone,
    };
  }

  static Customer fromMap(Map<String, dynamic> map) {
    return Customer(
      id: map['id'],
      name: map['name'],
      email: map['email'],
      phone: map['phone'],
    );
  }
}
