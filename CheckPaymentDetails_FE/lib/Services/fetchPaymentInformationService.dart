import 'package:dio/dio.dart';
import 'package:network_info_plus/network_info_plus.dart';
import 'package:payment_app/Services/urlmap.dart';
import 'package:flutter_dotenv/flutter_dotenv.dart';

Future<Response?> fetchPaymentAmounts({
  required DateTime selectedDay,
  required int nowIndex,
}) async {
  final dio = Dio();
  final String? ip = await NetworkInfo().getWifiIP();
  await dotenv.load(fileName: '.env');

  const periodMap = {
    0: "day",
    1: "month",
    2: "year",
  };

  final periodType = periodMap[nowIndex];
  String apiURL = '';

  if (ip != null && ip.startsWith('10.0.2')) {
    apiURL = 'http://10.0.2.2:8000/api/payments/$periodType/';
  } else {
    apiURL = 'http://$HOSTURL/api/payments/$periodType/';
  }

  print("API URL: $apiURL");

  try {
    final response = await dio.get(
      apiURL,
      queryParameters: {
        'Selected_Date': selectedDay.toString().substring(0, 10),
      },
      options: Options(
        headers: {'Content-Type': 'application/json'},
      ),
    );

    return response;

  } catch (e) {

    if (e is DioError) {
      print("Status: ${e.response?.statusCode}");
      print("Body: ${e.response?.data}");
    }
    return null;
  }
}
