import 'package:flutter/material.dart';
import 'package:payment_app/Services/loginService.dart';

import '../Routers/routingPoint.dart';

class LoginView extends StatefulWidget {
  const LoginView({super.key});

  @override
  State<LoginView> createState() => _LoginViewState();
}

class _LoginViewState extends State<LoginView> {
  final TextEditingController idController = TextEditingController();
  final TextEditingController pwController = TextEditingController();

  bool isLoading = false;
  String? errorMessage;

  Future<void> handleLogin(BuildContext context) async {
    setState(() {
      isLoading = true;
      errorMessage = null;
    });

    final id = idController.text.trim();
    final pw = pwController.text.trim();

    final response = await loginService(id: id, password: pw);

    setState(() => isLoading = false);

    if (response == null) {
      setState(() => errorMessage = "로그인 실패: 서버와의 연결 오류");
      return;
    }

    if (response.statusCode == 200) {
      final data = response.data;
      print("로그인 성공: $data");

      // 👉 프론트에서 토큰을 저장하지 않으므로 여기서 화면만 이동
      Navigator.push(
          context,
          RoutingPoint.generateRoute(
              settings: RouteSettings(
                  name: RoutingPoint.home
              )
          )
      );

    } else {
      setState(() => errorMessage = response.data["error"].toString());
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text("서비스 로그인"), backgroundColor: Colors.white),
      backgroundColor: Colors.white,
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          children: [
            const SizedBox(height: 200),
            TextField(
              controller: idController,
              decoration: const InputDecoration(labelText: "ID"),
            ),
            TextField(
              controller: pwController,
              decoration: const InputDecoration(labelText: "Password"),
              obscureText: true,
            ),

            const SizedBox(height: 20),

            if (errorMessage != null)
              Text(
                errorMessage!,
                style: const TextStyle(color: Colors.red),
              ),

            const SizedBox(height: 20),

            ElevatedButton(
              onPressed: isLoading ? null : () { handleLogin(context); },
              style: ElevatedButton.styleFrom(
                backgroundColor: Colors.cyan
              ),
              child: isLoading
                  ? const CircularProgressIndicator(color: Colors.white)
                  : const Text("로그인", style: TextStyle(
                color: Colors.black
              )),
            ),

            const SizedBox(height: 20),

            TextButton(
              onPressed: () {
                Navigator.push(
                    context,
                    RoutingPoint.generateRoute(
                        settings: RouteSettings(
                            name: RoutingPoint.signup
                        )
                    )
                );
              },
              child: const Text(
                "회원가입",
                style: TextStyle(
                  color: Colors.blue,
                  decoration: TextDecoration.underline,
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}

