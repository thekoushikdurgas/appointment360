"""
Models for payment and subscription management
"""
from django.db import models
from apps.accounts.models import AdminUser
from apps.core.models import TimeStampedModel


class Subscription(TimeStampedModel):
    """
    Subscription model for user plans
    """
    PLAN_CHOICES = [
        ('basic', 'Basic'),
        ('pro', 'Professional'),
        ('enterprise', 'Enterprise'),
    ]
    
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('cancelled', 'Cancelled'),
        ('expired', 'Expired'),
    ]
    
    user = models.ForeignKey(
        AdminUser,
        on_delete=models.CASCADE,
        related_name='subscriptions'
    )
    plan_id = models.CharField(max_length=100, help_text="Razorpay plan ID")
    subscription_id = models.CharField(max_length=100, unique=True, help_text="Razorpay subscription ID")
    plan_type = models.CharField(max_length=50, choices=PLAN_CHOICES)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='inactive')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10, default='INR')
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(blank=True, null=True)
    payment_id = models.CharField(max_length=100, blank=True, null=True)
    
    class Meta:
        db_table = 'subscriptions'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.email} - {self.plan_type} ({self.status})"


class PaymentTransaction(TimeStampedModel):
    """
    Payment transaction model
    """
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('success', 'Success'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ]
    
    user = models.ForeignKey(
        AdminUser,
        on_delete=models.CASCADE,
        related_name='payment_transactions'
    )
    subscription = models.ForeignKey(
        Subscription,
        on_delete=models.CASCADE,
        related_name='transactions',
        null=True,
        blank=True
    )
    razorpay_payment_id = models.CharField(max_length=100, unique=True)
    razorpay_order_id = models.CharField(max_length=100, blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10, default='INR')
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='pending')
    metadata = models.JSONField(default=dict, blank=True)
    
    class Meta:
        db_table = 'payment_transactions'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.email} - {self.razorpay_payment_id} ({self.status})"

