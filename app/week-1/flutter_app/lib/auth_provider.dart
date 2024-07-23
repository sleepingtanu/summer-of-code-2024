import 'package:flutter/material.dart';

class AuthProvider with ChangeNotifier {
  String _token = '';
  bool _isLoading = false;

  String get token => _token;
  bool get isLoading => _isLoading;

  void login(String token) {
    _token = token;
    _isLoading = false;
    notifyListeners();
  }

  void setLoading(bool isLoading) {
    _isLoading = isLoading;
    notifyListeners();
  }

  void logout() {
    _token = '';
    notifyListeners();
  }

  bool get isAuthenticated => _token.isNotEmpty;
}
