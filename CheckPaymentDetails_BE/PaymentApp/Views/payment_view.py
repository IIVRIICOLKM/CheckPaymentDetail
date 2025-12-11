import overrides
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from ..Models.payment import Payment
from ..Serializers.payment_serializer import PaymentSerializer
from rest_framework.permissions import AllowAny
from datetime import datetime, timedelta

# Test OK
# ORM Query Reference : https://diane073.tistory.com/158

class PaymentPerDay:
    __selected_period = 1

    def selected_period(self):
        return self.__selected_period

    class PaymentAmountView(APIView):
        permission_classes = [AllowAny]

        ## 테스트용 임시
        def get(self, request):
            try:
                __selected_period = PaymentPerDay.selected_period(PaymentPerDay())

                data = request.data
                last_date = datetime.strptime(data['Selected_Date'], '%Y-%m-%d').date()
                first_date = last_date - timedelta(days=__selected_period)
                preserialized_payments = Payment.objects.filter(payment_day__date__range=[first_date, last_date])
                serialized_payments = PaymentSerializer(instance=preserialized_payments, many=True)   # 파라미터(kwargs)랑 클래스 상속 관련 중요개념 많이 들어간 코드니 다시 한 번 확인하길
                payments = serialized_payments.data

                amount = 0

                for payment in payments:
                    if payment['amount'] < 0:
                        amount -= payment['amount']

                return Response(
                    data = {'consumption_amount': amount},
                    status=status.HTTP_200_OK
                )

            except Exception as e:
                return Response(
                    {
                        'error': 'failed',
                        'details': str(e)
                    },
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

class PaymentPerMonth:
    __selected_period = 30

    def selected_period(self):
        return self.__selected_period

    class PaymentAmountView(APIView):
        permission_classes = [AllowAny]

        ## 테스트용 임시
        def get(self, request):
            try:
                __selected_period = PaymentPerMonth.selected_period(PaymentPerMonth())

                data = request.data
                last_date = datetime.strptime(data['Selected_Date'], '%Y-%m-%d').date()
                first_date = last_date - timedelta(days=__selected_period)

                preserialized_payments = Payment.objects.filter(payment_day__date__range=[first_date, last_date])
                serialized_payments = PaymentSerializer(instance=preserialized_payments, many=True)   # 파라미터(kwargs)랑 클래스 상속 관련 중요개념 많이 들어간 코드니 다시 한 번 확인하길
                payments = serialized_payments.data

                amount = 0

                for payment in payments:
                    if payment['amount'] < 0:
                        amount -= payment['amount']

                return Response(
                    data = {'consumption_amount': amount},
                    status=status.HTTP_200_OK
                )

            except Exception as e:
                return Response(
                    {
                        'error': 'failed',
                        'details': str(e)
                    },
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

class PaymentPerYear:
    __selected_period = 365

    def selected_period(self):
        return self.__selected_period

    class PaymentAmountView(APIView):
        permission_classes = [AllowAny]

        ## 테스트용 임시
        def get(self, request):
            try:
                __selected_period = PaymentPerYear.selected_period(PaymentPerYear())

                data = request.data
                last_date = datetime.strptime(data['Selected_Date'], '%Y-%m-%d').date()
                first_date = last_date - timedelta(days=__selected_period)

                preserialized_payments = Payment.objects.filter(payment_day__date__range=[first_date, last_date])
                serialized_payments = PaymentSerializer(instance=preserialized_payments, many=True)   # 파라미터(kwargs)랑 클래스 상속 관련 중요개념 많이 들어간 코드니 다시 한 번 확인하길
                payments = serialized_payments.data

                amount = 0

                for payment in payments:
                    if payment['amount'] < 0:
                        amount -= payment['amount']

                return Response(
                    data = {'consumption_amount': amount},
                    status=status.HTTP_200_OK
                )

            except Exception as e:
                return Response(
                    {
                        'error': 'failed',
                        'details': str(e)
                    },
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )