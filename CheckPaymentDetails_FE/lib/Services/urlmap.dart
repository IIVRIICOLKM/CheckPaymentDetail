import 'package:flutter_dotenv/flutter_dotenv.dart';

final URLS = {
  'signup' : 'api/signup',
  'login' : 'api/login',
  'paymentsperday' : 'api/payments/day',
  'paymentspermonth' : 'api/payments/month',
  'paymentsperyear' : 'api/payments/year',
};

final HOSTURL = dotenv.env['HOSTURL'];