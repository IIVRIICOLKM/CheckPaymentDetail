import 'package:flutter/material.dart';
import 'package:payment_app/Widgets/appFrame.dart';
import 'package:payment_app/Widgets/statefulViews.dart';
import 'package:dio/dio.dart';
import 'package:payment_app/Services/fetchPaymentInformation.dart';

class HomeView extends StatelessWidget{
  HomeView(){}

  Widget build(BuildContext context){
    double screenWidth = MediaQuery.of(context).size.width;
    double screenHeight = MediaQuery.of(context).size.height;

    DateTime selectedDay = DateTime.now();
    PaymentInformation paymentInformation = PaymentInformation(selectedDay: selectedDay);
    TableCalendarScreen tableCalendarScreen = TableCalendarScreen();

    return Scaffold(
        body: Center(
            child: Column(
                mainAxisAlignment: MainAxisAlignment.start,
                children: <Widget>[
                  mainAppBar(name: appName),
                  SizedBox(height: 20),
                  Container(
                      height: screenHeight - 210,
                      width: screenWidth,
                      margin: EdgeInsets.symmetric(horizontal: 15),
                      padding: EdgeInsets.fromLTRB(20, 10, 20, 10),
                      decoration: BoxDecoration(
                        color: Colors.grey[300],
                        borderRadius: BorderRadius.circular(20)
                      ),
                      child: Stack(
                        children: [
                          Positioned(
                              right: 0,
                              child: IconButton(
                                icon: const Icon(Icons.calendar_month),
                                iconSize: 18,
                                alignment: Alignment.topRight,
                                onPressed: (){
                                  tableCalendarScreen = TableCalendarScreen();
                                  //Stateless 위젯 내부에서 onPressed 함수 내부에 빌더 패턴으로 다이얼로그로 덮기
                                  showDialog(
                                      context: context,
                                      builder: (context) => Dialog(
                                          child: Column(
                                            mainAxisAlignment: MainAxisAlignment.start,
                                            children: <Widget>[
                                              tableCalendarScreen,
                                              FilledButton(
                                                  onPressed: () async {
                                                    selectedDay = tableCalendarScreen.tableCalendarScreenState.selectedDay;
                                                    int nowIndex = paymentInformation.setSelectedDay(selectedDay: selectedDay).getNowIndex();
                                                    Response? response = await fetchPaymentAmounts(selectedDay: selectedDay, nowIndex: nowIndex);
                                                    paymentInformation.getResponseInThis(response);
                                                    Navigator.pop(context);
                                                  },
                                                  child: Text('확인')
                                              )
                                            ],
                                          )
                                      )
                                  );
                                },
                              )
                          ),
                          Positioned(
                            top: 70,
                            child: Container(
                              height: screenHeight - 310,
                              width: screenWidth - 70,
                              decoration: BoxDecoration(
                                borderRadius: BorderRadius.circular(20),
                                color: Colors.cyanAccent
                              ),
                              child: paymentInformation
                            )
                          ),
                          Positioned(
                            child: BankAccordion()
                          ),
                        ],
                      )
                  )
                ]
            )
        ),
        bottomNavigationBar: mainBottomBar()
    );
  }
}