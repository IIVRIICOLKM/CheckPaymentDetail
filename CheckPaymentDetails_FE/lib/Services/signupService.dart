import 'package:dio/dio.dart';
import 'package:network_info_plus/network_info_plus.dart';
import 'package:payment_app/Services/urlmap.dart';
import 'package:flutter_dotenv/flutter_dotenv.dart';

Future<Response?> signupService({
  required String id,
  required String password,
  required String name,
  required String registrationNumber,
}) async {
  final dio = Dio();
  final String? ip = await NetworkInfo().getWifiIP();
  await dotenv.load(fileName: '.env');
  String apiURL = '';

  // 에뮬레이터 환경 분기
  if (ip != null && ip.startsWith('10.0.2')) {
    apiURL = 'http://10.0.2.2:8000/' + URLS['signup']!;
  } else {
    apiURL = 'http://' + HOSTURL! + URLS['signup']!;
  }

  print("Signup API URL: $apiURL");

  try {
    final response = await dio.post(
      apiURL,
      data: {
        "id": id,
        "password": password,
        "name": name,
        "registration_number": registrationNumber,
      },
      options: Options(
        headers: {
          'Content-Type': 'application/json',
        },
      ),
    );

    return response;

  } catch (e) {
    print('Failed to signup... : $e');

    if (e is DioError) {
      print("Status Code: ${e.response?.statusCode}");
      print("Response: ${e.response?.data}");
    }

    return null;
  }
}
