import 'package:flutter/material.dart';

// 제작 페이지 등록
import '../Views/HomeView.dart';
import '../Views/LoginView.dart';
import '../Views/SignupView.dart';

class RoutingPoint {
  // 앱 전체 route 이름 관리
  static const String home = '/';
  static const String login = '/login';
  static const String signup = '/signup';

  // route → 화면 위젯 빌더 매핑
  static Route<dynamic> generateRoute(
      {
        required RouteSettings settings,
        final Map<String, dynamic>? result,
      })
  {

    switch (settings.name) {
      case home:
        return MaterialPageRoute(
          builder: (_) => HomeView(),
        );
      case login:
        return MaterialPageRoute(
          builder: (_) => LoginView(),
        );

      case signup:
        return MaterialPageRoute(
          builder: (_) => SignupView(),
      );

      default:
        return MaterialPageRoute(
          builder: (_) => const Scaffold(
            body: Center(
              child: Text('404 - Page not found'),
            ),
          ),
        );
    }
  }
}