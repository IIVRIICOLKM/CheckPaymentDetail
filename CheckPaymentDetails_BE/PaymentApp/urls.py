from django.urls import path

from .Views.payment_view import PaymentAmountView

urlpatterns = [
    path('api/payments/day', PaymentAmountView.as_view()),
    path('api/payments/month', PaymentAmountView.as_view()),
    path('api/payments/year', PaymentAmountView.as_view()),
]