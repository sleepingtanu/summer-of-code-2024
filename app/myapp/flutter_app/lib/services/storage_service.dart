import 'dart:io';
import 'package:firebase_storage/firebase_storage.dart';

class StorageService {
  final FirebaseStorage _storage = FirebaseStorage.instance;

  // Upload file to Firebase Storage
  Future<String> uploadFile(File file, String path) async {
    UploadTask uploadTask = _storage.ref().child(path).putFile(file);
    TaskSnapshot snapshot = await uploadTask;
    return await snapshot.ref.getDownloadURL();
  }

  // Get file download URL
  Future<String> getFileDownloadUrl(String path) async {
    return await _storage.ref().child(path).getDownloadURL();
  }
}
