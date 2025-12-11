import 'package:flutter/material.dart';

final String appName = 'PaymentApp';

class mainAppBar extends StatelessWidget{
  const mainAppBar({super.key, name});

  @override
  Widget build(BuildContext context) {
    return Container(
        height: 56,
        child: Scaffold(
          appBar : AppBar(backgroundColor: Colors.white, toolbarHeight: 0),
          body:
            Center(
              child: Column(
                mainAxisAlignment: MainAxisAlignment.start,
                children: <Widget>[
                  Container(
                    height : 30,
                    color: Colors.white,
                    child: Row(
                      mainAxisAlignment: MainAxisAlignment.start,
                      children: <Widget>[
                        SizedBox(width: 10),
                        Text(appName, style: const TextStyle(fontSize: 20, color: Colors.black, fontWeight: FontWeight.bold)),
                      ],
                    ),
                  ),
                  Container(
                      color: Colors.grey[700],
                      child: Divider(height: 1)
                  ),
                ]
              )
            )
        )
    );
  }
}

class mainBottomBar extends StatelessWidget{
  const mainBottomBar({super.key});

  void onItemTapped(int index){}

  @override
  Widget build(BuildContext context) {
    double screenWidth = MediaQuery.of(context).size.width;

    return SafeArea(
        child: Container(
            height: 60,
            width: screenWidth,
            child: BottomNavigationBar(
              onTap: onItemTapped,
              showSelectedLabels: false,
              showUnselectedLabels: false,
              type: BottomNavigationBarType.fixed,
              backgroundColor: Colors.white,
              selectedItemColor: Colors.black,
              items: const [
                BottomNavigationBarItem(icon: Icon(Icons.home), label:'home'),
                BottomNavigationBarItem(icon: Icon(Icons.star), label:'star'),
                BottomNavigationBarItem(icon: Icon(Icons.thumb_up), label:'thumb_up')
              ],
            )
        )
    );
  }
}