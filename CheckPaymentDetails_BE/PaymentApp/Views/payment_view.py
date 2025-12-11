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
                return Response(
                    {"error": "invalid period type"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            selected_period = self.PERIOD_MAP[period_type]

            # GET 요청에서 데이터는 request.query_params 로 받아야 함
            selected_date_str = request.query_params.get("Selected_Date")

            if not selected_date_str:
                return Response(
                    {"error": "Selected_Date is required"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            last_date = datetime.strptime(selected_date_str, "%Y-%m-%d").date()
            first_date = last_date - timedelta(days=selected_period)

            payments = Payment.objects.filter(
                payment_day__date__range=[first_date, last_date]
            )

            amount = sum(-p.amount for p in payments if p.amount < 0)

            return Response(
                {
                    "period": period_type,
                    "start_date": first_date,
                    "end_date": last_date,
                    "consumption_amount": amount
                },
                status=status.HTTP_200_OK
            )

        except Exception as e:
            return Response(
                {"error": "failed", "details": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

