from django.urls import path

from PaymentApp.Views.payment_view import PaymentPerDay
from PaymentApp.Views.payment_view import PaymentPerMonth
from PaymentApp.Views.payment_view import PaymentPerYear

urlpatterns = [
    path('api/payments/day', PaymentPerDay.PaymentAmountView.as_view(), name='payments_per_day_view'),
    path('api/payments/month', PaymentPerMonth.PaymentAmountView.as_view(), name='payments_per_month_view'),
    path('api/payments/year', PaymentPerYear.PaymentAmountView.as_view(), name='payments_per_year_view')
]