import 'package:dio/dio.dart';
import 'package:network_info_plus/network_info_plus.dart';
import 'package:flutter_dotenv/flutter_dotenv.dart';

final URLS = {
  'paymentsperday' : 'api/payments/day',
  'paymentspermonth' : 'api/payments/month',
  'paymentsperyear' : 'api/payments/year',
};

final HOSTURL = dotenv.env['HOSTURL'];