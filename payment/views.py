from django.shortcuts import render, redirect
from django.contrib import messages

# Create your views here.

def process_payment(request):
    if request.method == 'POST':
        # Here you would integrate with a payment gateway like Stripe, PayPal, etc.
        # For now, simulate a successful payment
        messages.success(request, 'Payment processed successfully!')
        return redirect('payment:payment_success')
    return render(request, 'payment/process.html')

def payment_success(request):
    return render(request, 'payment/success.html')
