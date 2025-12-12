from django.urls import path

from .Views.payment_view import PaymentAmountView, PaymentRangeAmountView
from .Views.login_view import LoginView, SignupView

urlpatterns = [
    path('api/signup', SignupView.as_view()),
    path('api/login', LoginView.as_view()),
    path('api/payments/<str:period_type>/', PaymentAmountView.as_view()),
    path("api/payments/range", PaymentRangeAmountView.as_view()),
]