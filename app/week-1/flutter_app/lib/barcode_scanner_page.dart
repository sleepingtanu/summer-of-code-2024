import 'package:flutter/material.dart';
import 'package:qr_code_scanner/qr_code_scanner.dart';
import 'package:permission_handler/permission_handler.dart';
import 'package:shared_preferences/shared_preferences.dart';

class BarcodeScannerPage extends StatefulWidget {
  const BarcodeScannerPage({Key? key}) : super(key: key);

  @override
  State<BarcodeScannerPage> createState() => _BarcodeScannerPageState();
}

class _BarcodeScannerPageState extends State<BarcodeScannerPage> {
  final GlobalKey qrKey = GlobalKey(debugLabel: 'QR');
  QRViewController? controller;
  List<String> scannedCodes = [];

  @override
  void initState() {
    super.initState();
    _loadScannedCodes();
    _checkPermissions();
  }

  Future<void> _checkPermissions() async {
    if (await Permission.camera.request().isGranted) {
      // Permission is granted
    } else {
      // Show message that permission is required
    }
  }

  Future<void> _loadScannedCodes() async {
    final prefs = await SharedPreferences.getInstance();
    setState(() {
      scannedCodes = prefs.getStringList('scannedCodes') ?? [];
    });
  }

  Future<void> _saveScannedCode(String code) async {
    final prefs = await SharedPreferences.getInstance();
    setState(() {
      scannedCodes.add(code);
      prefs.setStringList('scannedCodes', scannedCodes);
    });
  }

  @override
  void dispose() {
    controller?.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Barcode Scanner'),
      ),
      body: Column(
        children: [
          Expanded(
            flex: 4,
            child: QRView(
              key: qrKey,
              onQRViewCreated: _onQRViewCreated,
            ),
          ),
          Expanded(
            flex: 1,
            child: ListView.builder(
              itemCount: scannedCodes.length,
              itemBuilder: (context, index) {
                return ListTile(
                  title: Text(scannedCodes[index]),
                );
              },
            ),
          ),
        ],
      ),
    );
  }

  void _onQRViewCreated(QRViewController controller) {
    setState(() {
      this.controller = controller;
    });
    controller.scannedDataStream.listen((scanData) {
      _saveScannedCode(scanData.code ?? '');
    });
  }
}
