import 'package:flutter/material.dart';
import 'package:connectivity_plus/connectivity_plus.dart';
import 'dart:async';

class ConnectivityService extends ChangeNotifier {
  final Connectivity _connectivity = Connectivity();
  late StreamSubscription<List<ConnectivityResult>> _subscription;
  bool _isConnected = true;

  ConnectivityService() {
    _initConnectivity();
    _subscription =
        _connectivity.onConnectivityChanged.listen((results) {
      // Handle the list of results
      if (results.isNotEmpty) {
        _updateConnectionStatus(results.first);
      }
    });
  }

  bool get isConnected => _isConnected;

  Future<void> _initConnectivity() async {
    ConnectivityResult result;
    try {
      result = (await _connectivity.checkConnectivity()) as ConnectivityResult;
    } catch (e) {
      result = ConnectivityResult.none;
    }
    _updateConnectionStatus(result);
  }

  void _updateConnectionStatus(ConnectivityResult result) {
    _isConnected = result != ConnectivityResult.none;
    notifyListeners();
  }

  @override
  void dispose() {
    _subscription.cancel();
    super.dispose();
  }
}
