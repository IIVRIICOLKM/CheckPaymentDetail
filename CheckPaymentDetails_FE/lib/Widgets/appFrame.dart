import 'package:flutter/material.dart';

import '../Routers/routingPoint.dart';

const String appName = 'PaymentApp';

class mainAppBar extends StatelessWidget{
  const mainAppBar({super.key, name});

  @override
  Widget build(BuildContext context) {
    return Container(
        height: 90,
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
                        const SizedBox(width: 10),
                        const Text(appName, style: const TextStyle(fontSize: 20, color: Colors.black, fontWeight: FontWeight.bold)),
                        const SizedBox(width : 190),
                        IconButton(
                          onPressed: (){
                            Navigator.push(
                                context,
                                RoutingPoint.generateRoute(
                                    settings: RouteSettings(
                                        name: RoutingPoint.setting
                                    )
                                )
                            );
                          },
                          icon: Icon(Icons.settings)
                        )
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