import 'package:dio/dio.dart';
import 'package:network_info_plus/network_info_plus.dart';
import 'package:payment_app/Services/urlmap.dart';
import 'package:flutter_dotenv/flutter_dotenv.dart';

Future<Response?> loginService({
  required String id,
  required String password,
}) async {
  final dio = Dio();
  final String? ip = await NetworkInfo().getWifiIP();
  await dotenv.load(fileName: '.env');
  String apiURL = '';

  // 👉 에뮬레이터 환경 분기
  if (ip != null && ip.startsWith('10.0.2')) {
    apiURL = 'http://10.0.2.2:8000/' + URLS['login']!;
  } else {
    apiURL = 'http://' + HOSTURL! + URLS['login']!;
  }

  print("Login API URL: $apiURL");
  final response;
  try {
    response = await dio.post(
      apiURL,
      data: {
        "id": id,
        "password": password,
      },
      options: Options(
        headers: {
          'Content-Type': 'application/json',
        },
      ),
    );

    return response;

  } catch (e) {
    print('Failed to login... : $e');

    if (e is DioException) {
      print("Status Code: ${e.response?.statusCode}");
      print("Response: ${e.response?.data}");
      return e.response;
    }
    else {
      return null;
    }
  }
}
