import 'package:dio/dio.dart';
import 'package:network_info_plus/network_info_plus.dart';
import 'package:payment_app/Services/urlmap.dart';
import 'package:flutter_dotenv/flutter_dotenv.dart';

Future<Response?> fetchPaymentAmounts({required DateTime selectedDay, required int nowIndex}) async {
  final dio = Dio();
  final String? ip = await NetworkInfo().getWifiIP();
  await dotenv.load(fileName: '.env');
  String apiURL = '';

  if (ip!.startsWith('10.0.2')){
    if (nowIndex == 0)
      apiURL = 'http://10.0.2.2:8000/' + URLS['paymentsperday']!;
    else if (nowIndex == 1)
      apiURL = 'http://10.0.2.2:8000/' + URLS['paymentspermonth']!;
    else
      apiURL = 'http://10.0.2.2:8000/' + URLS['paymentsperyear']!;
  }
  else{
    if (nowIndex == 0)
      apiURL = 'http://' + HOSTURL! + URLS['paymentsperday']!;
    else if (nowIndex == 1)
      apiURL = 'http://' + HOSTURL! + URLS['paymentspermonth']!;
    else
      apiURL = 'http://' + HOSTURL! + URLS['paymentsperyear']!;
  }

  print(apiURL);

  try {
    final response = await dio.get(
      apiURL,
      data: {
        'Selected_Date': selectedDay.toString().substring(0, 10),
      },
      options: Options(
        headers: {
          'Content-Type': 'application/json',
        },
      ),
    );

    return response;

  } catch (e) {
    print('failed to fetching payment datas... : ${e}');
    if (e is DioError) {
      print('Status: ${e.response?.statusCode}');
      print('Message: ${e.response?.data}');
    } else {
      print(e.toString());
    }
    return null;
  }
}