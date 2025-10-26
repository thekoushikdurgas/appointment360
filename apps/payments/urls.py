"""
URL configuration for payments app
"""
from django.urls import path
from .views import (
    get_plans, create_subscription, payment_webhook,
    subscribe_view, payment_view, razorpay_payment_view,
    payment_success_view, payment_failure_view, payment_callback_view
)

app_name = 'payments'

urlpatterns = [
    # API endpoints
    path('api/payments/plans/', get_plans, name='get-plans'),
    path('api/payments/subscribe/', create_subscription, name='create-subscription'),
    path('api/payments/webhook/', payment_webhook, name='payment-webhook'),
    
    # Web-based views
    path('subscribe/', subscribe_view, name='subscribe'),
    path('payment/', payment_view, name='payment'),
    path('razorpay/', razorpay_payment_view, name='razorpay'),
    path('success/', payment_success_view, name='success'),
    path('failure/', payment_failure_view, name='failure'),
    path('callback/', payment_callback_view, name='callback'),
]

