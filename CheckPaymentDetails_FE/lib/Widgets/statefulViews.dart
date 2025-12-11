import 'package:flutter/material.dart';
import 'package:payment_app/Services/fetchPaymentInformation.dart';
import 'package:provider/provider.dart';
import 'package:table_calendar/table_calendar.dart';
import 'package:dio/dio.dart';

// Bank Tab
class Bank{
  Bank({
    required this.headerValue,
    this.isExpanded = false,
  });

  String headerValue;
  bool isExpanded;
}

class BankAccordion extends StatefulWidget {
  const BankAccordion({super.key});

  @override
  State<BankAccordion> createState() => _BankAccordion();
}

/// MyStatefulWidget의 개인 상태 클래스입니다.
/// SingleChildScrollView로 ExpansionPanelList를 감쌉니다.
class _BankAccordion extends State<BankAccordion> {

  @override
  void dispose() {
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Container(
        width: 100,
        decoration: BoxDecoration(
          borderRadius: BorderRadius.circular(10),
          color: Colors.grey[100],
        ),
        child: ExpansionTile(
          title: Text('은행 정보', style: TextStyle(fontSize: 10)),
          minTileHeight: 10,
          tilePadding: EdgeInsets.symmetric(horizontal: 5.0),
          children: <Widget>[
            for(int i = 0; i < 5; i++)
              Container(
                  width: 120,
                  child: FilledButton(
                      onPressed: () async {

                      },
                      child: Text('버튼 $i', style: TextStyle(color: Colors.black)),
                      style: FilledButton.styleFrom(
                          backgroundColor: Colors.grey[100]
                      )
                  )
              )
          ],
        )
    );
  }
}

// Tab Screen
class TabBarScreen extends StatefulWidget with ChangeNotifier{
  TabBarScreen({Key? key}) : super(key: key);
  int nowIndex = 0;
  DateTime _selectedDay = DateTime.now();
  Response? response;

  Future<Response?> getResponseByTabBar() async {
    this.response = await fetchPaymentAmounts(selectedDay: _selectedDay, nowIndex: nowIndex);
  }

  void updateIndex(TabController tabController) async {
    nowIndex = tabController.index;
    await getResponseByTabBar();
    notifyListeners();
  }

  void setSelectedDay({required DateTime selectedDay}){
    this._selectedDay = selectedDay;
    notifyListeners();
  }

  @override
  State<TabBarScreen> createState() => _TabBarScreenState();
}

class _TabBarScreenState extends State<TabBarScreen> with TickerProviderStateMixin{
  late TabController tabController = TabController(
    length: 3,
    vsync: this,
    initialIndex: 0,
    /// 탭 변경 애니메이션 시간
    animationDuration: const Duration(milliseconds: 800),
  );

  @override
  void initState(){
    super.initState();
  }

  @override
  void dispose() {
    tabController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return _tabBar();
  }
  // TabController -> controller which shows information of tabbar
  Widget _tabBar() {
    return TabBar(
        controller: tabController,
        tabs: const [
          Tab(text: "일별"),
          Tab(text: "월별"),
          Tab(text: "연별"),
        ],
        labelColor: Colors.black,
        labelStyle: const TextStyle(
            fontSize: 18,
            fontWeight: FontWeight.bold
        ),
        unselectedLabelColor: Colors.grey,
        unselectedLabelStyle: const TextStyle(
            fontSize: 16
        ),
        indicatorColor: Colors.black,
        indicatorWeight: 5,
        indicatorSize: TabBarIndicatorSize.tab,
        onTap: (index) => {
          setState(() {
            widget.updateIndex(this.tabController);
          })
        }
    );
  }
}

// Payment Information Frame

class PaymentInformation extends StatefulWidget with ChangeNotifier{

  TabBarScreen tabBarScreen = TabBarScreen();
  DateTime? selectedDay;
  Response? response;

  PaymentInformation({super.key, required DateTime selectedDay}){
    this.selectedDay = selectedDay;
  }

  PaymentInformation setSelectedDay({required DateTime selectedDay}){
    this.selectedDay = selectedDay;
    tabBarScreen.setSelectedDay(selectedDay: selectedDay);
    notifyListeners();
    return this;
  }

  int getNowIndex(){
    return tabBarScreen.nowIndex;
  }

  void getResponseInThis(Response? response){
    this.response = response;
    notifyListeners();
  }

  @override
  State<PaymentInformation> createState() => _PaymentInformationState();
}

class _PaymentInformationState extends State<PaymentInformation>{

  @override
  void initState(){
    super.initState();
  }

  // 하나의 build 함수 내부에서 Provider를 소비, 생산을 동시에 하는 경우 Consumer 메서드 사용
  // 아닌 경우 context.read, watch<T>().Func 패턴 사용

  //경고 : build 함수 자체는 rebuild x
  @override
  Widget build(BuildContext context) {
    return Column(
      mainAxisAlignment: MainAxisAlignment.start,
      children: [
        widget.tabBarScreen,
        SizedBox(height: 40),
        ChangeNotifierProvider<PaymentInformation>.value(
          value: widget,
          child: Consumer<PaymentInformation>(
              builder: (_, _, _){
                return PaymentPresentation(tabBarScreen: widget.tabBarScreen, selectedDay: widget.selectedDay!, response: widget.response);
              }
          ),
        )
      ],
    );
  }
}

// Payment Information

class PaymentPresentation extends StatefulWidget{

  TabBarScreen? tabBarScreen;
  DateTime? selectedDay;
  Response? response;

  PaymentPresentation({super.key, required TabBarScreen tabBarScreen, required DateTime selectedDay, Response? response}){
    this.tabBarScreen = tabBarScreen;
    this.selectedDay = selectedDay;
    this.response = response;
  }

  void checkResponseByTabBar(TabBarScreen tabscr){
    if (tabscr.response != null)
      this.response = tabscr.response;
    tabscr.response = null;
  }

  @override
  State<PaymentPresentation> createState() => _PaymentPresentationState();
}

//경고 : build 함수 자체는 rebuild x
class _PaymentPresentationState extends State<PaymentPresentation>{

  Widget build(BuildContext context){
    DateTime oneMonthAgo = widget.selectedDay!.subtract(Duration(days: 31));
    DateTime oneYearAgo = widget.selectedDay!.subtract(Duration(days: 365));

    return ChangeNotifierProvider<TabBarScreen>.value(
      value: widget.tabBarScreen!,
      // Consumer로 타 클래스에 있는 상태값에 따라 위젯 변경 가능, ChangeNotifierProvider가 다른 build 함수에 있는 경우에는 context.watch<T>().func
      child: Consumer<TabBarScreen>(
          builder: (context, tabscr, child){
            widget.checkResponseByTabBar(tabscr);
            return Column(
              mainAxisAlignment: MainAxisAlignment.start,
              children: <Widget>[
                if (tabscr.nowIndex == 0)
                  Text('${widget.selectedDay!.year}년 ${widget.selectedDay!.month}월 ${widget.selectedDay!.day}일의 소비 내역입니다.')
                else if (tabscr.nowIndex == 1)
                  Text('${oneMonthAgo.year}년 ${oneMonthAgo.month}월 ${oneMonthAgo.day}일 부터 '
                      '${widget.selectedDay!.year}년 ${widget.selectedDay!.month}월 ${widget.selectedDay!.day}일 까지의 소비내역입니다.')
                else
                  Text('${oneYearAgo.year}년 ${oneYearAgo.month}월 ${oneYearAgo.day}일 부터 '
                      '${widget.selectedDay!.year}년 ${widget.selectedDay!.month}월 ${widget.selectedDay!.day}일 까지의 소비내역입니다.'),
                if (widget.response != null)
                  Text('총 소비액은 ${widget.response!.data['consumption_amount']}원 입니다.'),
                SizedBox(height: 40),
                Container(
                  width: 300,
                  height: 300,
                  padding: EdgeInsets.all(20),
                  color: Colors.greenAccent,
                ),
                Divider(height: 2, color: Colors.black)
              ],
            );
          }
      ),
    );
  }
}

// Calender

class TableCalendarScreen extends StatefulWidget {
  TableCalendarScreen({super.key});
  _TableCalendarScreenState tableCalendarScreenState = _TableCalendarScreenState();

  @override
  State<TableCalendarScreen> createState() => tableCalendarScreenState;
}

class _TableCalendarScreenState extends State<TableCalendarScreen> {

  DateTime _selectedDay = DateTime(
    DateTime.now().year,
    DateTime.now().month,
    DateTime.now().day,
  );

  DateTime _focusedDay = DateTime.now();
  DateTime get selectedDay => _selectedDay;

  @override
  Widget build(BuildContext context) {
    return TableCalendar(
      locale: 'en_US',
      firstDay: DateTime.utc(2019, 01, 01),
      lastDay: DateTime.utc(2025, 12, 31),
      focusedDay: _focusedDay,
      headerStyle: HeaderStyle(
        formatButtonVisible: false,
        titleCentered: true,
      ),
      onDaySelected: (selectedDay, focusedDay) {
        // 선택된 날짜의 상태를 갱신합니다.
        setState((){
          this._selectedDay = selectedDay;
          this._focusedDay = focusedDay;
        });
      },
      selectedDayPredicate: (day) {
        // selectedDay 와 동일한 날짜의 모양을 바꿔줍니다.
        return isSameDay(_selectedDay, day);
      },
    );
  }
}