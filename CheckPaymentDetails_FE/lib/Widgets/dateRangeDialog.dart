import 'package:flutter/material.dart';

Future<DateTimeRange?> showDateRangePickerDialog(BuildContext context) {
  return showDateRangePicker(
    context: context,
    firstDate: DateTime(2019, 1, 1),
    lastDate: DateTime.now(),
    initialDateRange: DateTimeRange(
      start: DateTime.now().subtract(const Duration(days: 7)),
      end: DateTime.now(),
    ),
    helpText: '조회 기간 선택',
    cancelText: '취소',
    confirmText: '확인',
  );
}
