from django.urls import path

from .Views.payment_view import PaymentAmountView
from .Views.login_view import LoginView, SignupView

urlpatterns = [
    path('api/signup', SignupView.as_view()),
    path('api/login', LoginView.as_view()),
    path('api/payments/day', PaymentAmountView.as_view()),
    path('api/payments/month', PaymentAmountView.as_view()),
    path('api/payments/year', PaymentAmountView.as_view()),
]