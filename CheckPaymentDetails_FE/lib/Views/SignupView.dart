import 'package:flutter/material.dart';
import 'package:payment_app/Services/signupService.dart';

import '../Routers/routingPoint.dart';

class SignupView extends StatefulWidget {
  const SignupView({super.key});

  @override
  State<SignupView> createState() => _SignupViewState();
}

class _SignupViewState extends State<SignupView> {
  final TextEditingController idController = TextEditingController();
  final TextEditingController pwController = TextEditingController();
  final TextEditingController nameController = TextEditingController();
  final TextEditingController regController = TextEditingController(); // 주민번호

  bool isLoading = false;
  String? errorMessage;

  Future<void> handleSignup(BuildContext context) async {
    setState(() {
      isLoading = true;
      errorMessage = null;
    });

    final id = idController.text.trim();
    final pw = pwController.text.trim();
    final name = nameController.text.trim();
    final reg = regController.text.trim();

    final response = await signupService(
      id: id,
      password: pw,
      name: name,
      registrationNumber: reg,
    );

    setState(() => isLoading = false);

    if (response == null) {
      setState(() => errorMessage = "회원가입 실패: 서버 연결 오류");
      return;
    }

    if (response.statusCode == 201) {
      print("회원가입 성공: ${response.data}");

      // 회원가입 성공 → 로그인 화면 또는 홈 화면으로 이동
      Navigator.push(
          context,
          RoutingPoint.generateRoute(
              settings: RouteSettings(
                  name: RoutingPoint.login
              )
          )
      );

    } else {
      // 서버에서 온 에러 메시지 표시
      setState(() => errorMessage = response.data.toString());
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text("회원가입"), backgroundColor: Colors.white),
      backgroundColor: Colors.white,
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: SingleChildScrollView(
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
              TextField(
                controller: nameController,
                decoration: const InputDecoration(labelText: "이름"),
              ),
              TextField(
                controller: regController,
                decoration: const InputDecoration(labelText: "주민등록번호"),
              ),

              const SizedBox(height: 20),

              if (errorMessage != null)
                Text(
                  errorMessage!,
                  style: const TextStyle(color: Colors.red),
                ),

              const SizedBox(height: 20),

              ElevatedButton(
                onPressed: isLoading ? null : (){handleSignup(context);},
                style: ElevatedButton.styleFrom(
                    backgroundColor: Colors.cyan
                ),
                child: isLoading
                    ? const CircularProgressIndicator(color: Colors.white)
                    : const Text("회원가입", style: TextStyle(
                    color: Colors.black),
                ),
              )
            ],
          ),
        ),
      ),
    );
  }
}
