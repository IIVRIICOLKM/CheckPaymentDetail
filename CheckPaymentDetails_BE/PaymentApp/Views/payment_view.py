from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from ..Models.payment import Payment
from rest_framework.permissions import AllowAny
from datetime import datetime, timedelta

# Test OK
# ORM Query Reference : https://diane073.tistory.com/158

class PaymentAmountView(APIView):
    permission_classes = [AllowAny]

    PERIOD_MAP = {
        "day": 1,
        "month": 30,
        "year": 365,
    }

    def get(self, request, period_type):
        try:
            if period_type not in self.PERIOD_MAP:
                return Response({"error": "invalid period type"}, status=status.HTTP_400_BAD_REQUEST)

            selected_date_str = request.query_params.get("Selected_Date")
            if not selected_date_str:
                return Response({"error": "Selected_Date is required"}, status=status.HTTP_400_BAD_REQUEST)

            selected_period = self.PERIOD_MAP[period_type]
            last_date = datetime.strptime(selected_date_str, "%Y-%m-%d").date()
            first_date = last_date - timedelta(days=selected_period)

            payments = Payment.objects.filter(
                payment_day__date__range=[first_date, last_date],
                amount__lt=0
            )

            total_amount = 0
            category_breakdown = {}

            for p in payments:
                place = p.place_id
                cat = place.place_category_id  # PlaceCategory 객체 or tuple

                # ✅ 문자열 카테고리명으로 정규화
                if hasattr(cat, "name"):
                    category_name = cat.name
                elif isinstance(cat, tuple):
                    category_name = cat[1] if len(cat) > 1 else str(cat[0])
                else:
                    category_name = str(cat)

                if category_name == "금융":
                    continue

                spend = -p.amount
                total_amount += spend
                category_breakdown[category_name] = category_breakdown.get(category_name, 0) + spend

            return Response(
                {
                    "period": period_type,
                    "start_date": first_date,
                    "end_date": last_date,
                    "total_consumption_amount": total_amount,
                    "category_breakdown": category_breakdown
                },
                status=status.HTTP_200_OK
            )

        except Exception as e:
            return Response({"error": "failed", "details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class PaymentRangeAmountView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        try:
            start_date_str = request.query_params.get("start_date")
            end_date_str = request.query_params.get("end_date")

            if not start_date_str or not end_date_str:
                return Response(
                    {"error": "start_date and end_date are required"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
            end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()

            if start_date > end_date:
                return Response(
                    {"error": "start_date must be before end_date"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            payments = Payment.objects.filter(
                payment_day__date__range=[start_date, end_date],
                amount__lt=0  # 출금만
            ).select_related("place_id__place_category_id")

            total_amount = 0
            category_breakdown = {}

            for p in payments:
                place = p.place_id
                category_obj = place.place_category_id
                category_name = category_obj.name

                # 금융 카테고리는 제외
                if category_name == "금융":
                    continue

                spend = -p.amount
                total_amount += spend
                category_breakdown[category_name] = (
                    category_breakdown.get(category_name, 0) + spend
                )

            return Response(
                {
                    "period": "range",
                    "start_date": start_date,
                    "end_date": end_date,
                    "total_consumption_amount": total_amount,
                    "category_breakdown": category_breakdown,
                },
                status=status.HTTP_200_OK
            )

        except Exception as e:
            return Response(
                {"error": "failed", "details": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )