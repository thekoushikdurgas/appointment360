"""
Views for payment and subscription management
"""
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import Subscription, PaymentTransaction
import razorpay
import logging
import uuid
from datetime import datetime

logger = logging.getLogger(__name__)

# Web-based views
@login_required
def subscribe_view(request):
    """
    Display subscription page with plans
    """
    try:
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY, settings.RAZORPAY_SECRET))
        plans_data = client.plan.all()
        
        # Mock plans for display if Razorpay is not configured
        plans = []
        for plan_item in plans_data.get('items', []):
            plans.append({
                'id': plan_item['id'],
                'name': plan_item['item']['name'],
                'amount': plan_item['item']['amount'] / 100,  # Convert paise to rupees
                'description': plan_item['item'].get('description', ''),
            })
        
        # If no plans from Razorpay, use mock data
        if not plans:
            plans = [
                {'id': 'basic', 'name': 'Basic Plan', 'amount': 499, 'description': 'Basic features'},
                {'id': 'pro', 'name': 'Pro Plan', 'amount': 999, 'description': 'Professional features'},
                {'id': 'enterprise', 'name': 'Enterprise Plan', 'amount': 1999, 'description': 'Enterprise features'},
            ]
        
        return render(request, 'payment/subscribe.html', {'plans': plans})
    except Exception as e:
        logger.error(f"Error fetching plans: {str(e)}")
        messages.error(request, 'Unable to load subscription plans. Please try again later.')
        return render(request, 'payment/subscribe.html', {'plans': []})


@login_required
def payment_view(request):
    """
    Display payment page
    """
    razorpay_key = getattr(settings, 'RAZORPAY_KEY', '')
    return render(request, 'payment/payment.html', {'razorpay_key': razorpay_key})


@login_required
def razorpay_payment_view(request):
    """
    Handle Razorpay payment redirect
    """
    if request.method == 'POST':
        try:
            plan_id = request.POST.get('plan')
            plan_amount = request.POST.get('plan_amount')
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            email = request.POST.get('email')
            phone = request.POST.get('phone', '')
            addon_amount = int(request.POST.get('addon_amount', 0))
            
            # Calculate total amount
            total_amount = int(plan_amount) + addon_amount
            amount_in_paise = total_amount * 100
            
            # Generate unique transaction ID
            txnid = str(uuid.uuid4())[:10]
            order_id = f"ORDER_{txnid}"
            
            # Create Razorpay order
            client = razorpay.Client(auth=(settings.RAZORPAY_KEY, settings.RAZORPAY_SECRET))
            
            # Create subscription with Razorpay
            subscription_data = {
                'plan_id': plan_id,
                'customer_notify': 1,
                'total_count': 12,  # 12 billing cycles
            }
            subscription = client.subscription.create(subscription_data)
            
            context = {
                'razorpay_key': settings.RAZORPAY_KEY,
                'txnid': txnid,
                'productinfo': f'Subscription Plan - {plan_amount}',
                'success_url': f"http://{request.get_host()}/payment/success/",
                'failure_url': f"http://{request.get_host()}/payment/failure/",
                'order_id': order_id,
                'name': f"{first_name} {last_name}",
                'email': email,
                'phone': phone,
                'amount': total_amount,
                'plan_id': plan_id,
                'subscription_id': subscription['id'],
                'package': 'Appointment360 Subscription',
                'return_url': f"http://{request.get_host()}/payment/callback/",
            }
            
            return render(request, 'payment/razorpay.html', context)
        except Exception as e:
            logger.error(f"Payment error: {str(e)}")
            messages.error(request, f'Payment error: {str(e)}')
            return redirect('payments:subscribe')
    
    return redirect('payments:subscribe')


@login_required
def payment_success_view(request):
    """
    Handle successful payment
    """
    payment_id = request.POST.get('razorpay_payment_id')
    order_id = request.POST.get('merchant_order_id')
    
    context = {
        'transaction_id': payment_id or order_id,
    }
    
    try:
        # Save payment transaction
        if payment_id:
            PaymentTransaction.objects.update_or_create(
                razorpay_payment_id=payment_id,
                defaults={
                    'user': request.user,
                    'razorpay_order_id': order_id,
                    'amount': 0,  # Will be updated via webhook
                    'status': 'success'
                }
            )
            
            # Update subscription
            subscription_id = request.POST.get('merchant_subscription_id')
            if subscription_id:
                Subscription.objects.filter(subscription_id=subscription_id).update(
                    payment_id=payment_id,
                    status='active'
                )
    except Exception as e:
        logger.error(f"Error processing payment success: {str(e)}")
    
    return render(request, 'payment/success.html', context)


@login_required
def payment_failure_view(request):
    """
    Handle failed payment
    """
    error_message = request.GET.get('error', 'Payment could not be processed.')
    
    context = {
        'error_message': error_message,
    }
    
    return render(request, 'payment/failure.html', context)


@login_required
def payment_callback_view(request):
    """
    Handle Razorpay callback after payment
    """
    try:
        payment_id = request.POST.get('razorpay_payment_id')
        
        if payment_id:
            # Payment successful
            return redirect('payments:success')
        else:
            # Payment failed
            return redirect('payments:failure')
    except Exception as e:
        logger.error(f"Callback error: {str(e)}")
        messages.error(request, 'Unable to process payment callback.')
        return redirect('payments:failure')


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_plans(request):
    """
    Get available subscription plans from Razorpay
    """
    try:
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY, settings.RAZORPAY_SECRET))
        plans = client.plan.all()
        
        return Response({
            'success': True,
            'plans': plans
        })
    except Exception as e:
        logger.error(f"Error fetching plans: {str(e)}")
        return Response({
            'success': False,
            'message': f'Error fetching plans: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_subscription(request):
    """
    Create a subscription
    """
    try:
        plan_id = request.data.get('plan_id')
        if not plan_id:
            return Response({
                'success': False,
                'message': 'Plan ID is required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY, settings.RAZORPAY_SECRET))
        
        subscription_data = {
            'plan_id': plan_id,
            'customer_notify': 1,
            'total_count': 12,  # 12 billing cycles (1 year)
        }
        
        subscription = client.subscription.create(subscription_data)
        
        # Save subscription to database
        subscription_obj = Subscription.objects.create(
            user=request.user,
            plan_id=plan_id,
            subscription_id=subscription['id'],
            plan_type=request.data.get('plan_type', 'basic'),
            status='active',
            amount=subscription.get('amount', 0),
            start_date=subscription.get('created_at')
        )
        
        return Response({
            'success': True,
            'subscription': subscription,
            'subscription_id': subscription['id']
        })
        
    except Exception as e:
        logger.error(f"Error creating subscription: {str(e)}")
        return Response({
            'success': False,
            'message': f'Error creating subscription: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([AllowAny])
def payment_webhook(request):
    """
    Handle Razorpay webhook events
    """
    try:
        payload = request.body
        sig_header = request.META.get('HTTP_X_RAZORPAY_SIGNATURE')
        
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY, settings.RAZORPAY_SECRET))
        
        # Verify webhook signature
        event = client.webhook.verify(payload, sig_header, settings.RAZORPAY_WEBHOOK_SECRET)
        
        event_type = event.get('event')
        payload_data = event.get('payload', {}).get('payment', {}).get('entity', {})
        
        if event_type == 'payment.captured':
            # Handle successful payment
            payment_id = payload_data.get('id')
            order_id = payload_data.get('order_id')
            
            # Save payment transaction
            PaymentTransaction.objects.get_or_create(
                razorpay_payment_id=payment_id,
                defaults={
                    'user': request.user if request.user.is_authenticated else None,
                    'razorpay_order_id': order_id,
                    'amount': payload_data.get('amount', 0) / 100,
                    'status': 'success'
                }
            )
            
            logger.info(f"Payment captured: {payment_id}")
        
        return Response({'success': True})
        
    except Exception as e:
        logger.error(f"Webhook error: {str(e)}")
        return Response({
            'success': False,
            'message': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)

