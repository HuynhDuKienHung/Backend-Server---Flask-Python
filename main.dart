import 'dart:io';

void main() async {
  String hostname = 'DESKTOP-81ODHIO';
  try {
    List<InternetAddress> addresses = await InternetAddress.lookup(hostname);
    if (addresses.isNotEmpty) {
      for (InternetAddress address in addresses) {
        print('Địa chỉ IP cho $hostname: ${address.address}');
        List<String> Element = ["https://", address.address, ":5000"];
        String ServerIP = Element.join("");
        print(ServerIP);
      }
    } else {
      print('Không tìm thấy địa chỉ IP cho $hostname');
    }
  } catch (e) {
    print('Lỗi: $e');
  }
}
