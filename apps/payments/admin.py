"""
Admin configuration for payment models
"""
from django.contrib import admin
from .models import Subscription, PaymentTransaction


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    """Admin interface for Subscription model"""
    list_display = (
        'user', 'plan_type', 'status', 'amount', 'currency',
        'start_date', 'end_date', 'created_at'
    )
    list_filter = ('status', 'plan_type', 'created_at', 'start_date')
    search_fields = ('user__email', 'subscription_id', 'plan_id')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)


@admin.register(PaymentTransaction)
class PaymentTransactionAdmin(admin.ModelAdmin):
    """Admin interface for PaymentTransaction model"""
    list_display = (
        'user', 'status', 'amount', 'currency',
        'razorpay_payment_id', 'razorpay_order_id', 'created_at'
    )
    list_filter = ('status', 'created_at')
    search_fields = ('user__email', 'razorpay_payment_id', 'razorpay_order_id')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)

