
import razorpay

from decouple import config

from django.db import transaction

from django.views.decorators.csrf import csrf_exempt

from django.utils.decorators import method_decorator

import datetime 

from atheletes. models import Users

from events. models import SportsEvent

from django.contrib.auth.decorators import login_required

from django.utils.dateparse import parse_date

from django.shortcuts import render, get_object_or_404, redirect

from django.conf import settings

from payments.models import Payment, Transactions

from django.utils import timezone

from django.http import HttpResponse

from students.models import ProfileDetails

from django.views.generic import View

from django.contrib.auth.mixins import LoginRequiredMixin

class PaymentDetailView(View):
    def get(self, request, uuid, *args, **kwargs):
        # Get the ProfileDetails based on the UUID
        event = get_object_or_404(ProfileDetails, uuid=uuid)

        # Retrieve the corresponding Payment record
        payment = Payment.objects.filter(event=event).first()

        # Retrieve the corresponding Transaction record, if payment exists
        transaction = Transactions.objects.filter(payment=payment).first() if payment else None

        # Pass the data to the template
        return render(request, 'payments/payment-details.html', {
            'event': event,
            'payment': payment,
            'transaction': transaction,
        })



class PaymentListView(View):
    
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):

        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')

        if request.user.is_superuser:  # Check if user is admin
            payments = Payment.objects.all()
        else:
            user = Users.objects.get(profile=request.user)
            payments = Payment.objects.filter(user=user)  # Regular user can only see their payments

        if start_date:
            payments = payments.filter(paid_at__gte=parse_date(start_date))

        if end_date:
            payments = payments.filter(paid_at__lte=parse_date(end_date))

        payments = payments.order_by('-created_at')

        return render(request, 'payments/payment-list.html', {'payments': payments})





class CombinedPaymentTransactionView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        user = Users.objects.filter(profile=request.user).first()

        if user:
            transactions = Transactions.objects.select_related('payment', 'payment__event', 'payment__student')\
                                               .filter(payment__student=user)
            return render(request, 'payments/transaction-details.html', {
                'transactions': transactions
            })
        else:
            return render(request, 'payments/transaction-details.html', {
                'error': 'No transactions found for this user.'
            })
    


class RazorpayView(View):
    def get(self, request, uuid, *args, **kwargs):
        # Find the current user's extended profile (Users model)
        user = Users.objects.filter(profile=request.user).first()
        if not user:
            return redirect('students-view')  # or 'login' or a proper fallback

        # Fetch the ProfileDetails using UUID and ensure it belongs to the current user
        registration = get_object_or_404(ProfileDetails, uuid=uuid, student=user)

        # Create Razorpay client
        client = razorpay.Client(auth=(settings.RZP_CLIENT_ID, settings.RZP_CLIENT_SECRET))

        # Prepare payment amount (Razorpay expects paise)
        amount_in_paise = int(float(registration.registration_fee) * 100)
        receipt_id = f"receipt_{str(registration.uuid)[:32]}"

        # Create Razorpay order
        order_data = {
            "amount": amount_in_paise,
            "currency": "INR",
            "receipt": receipt_id,
        }
        rzp_order = client.order.create(data=order_data)

        # Create a Payment record if not already created
        payment, created = Payment.objects.get_or_create(
            student=user,
            event=registration,
            defaults={
                "amount": registration.registration_fee,
                "status": "Pending",
            }
        )

        # Create a transaction
        Transactions.objects.create(
            payment=payment,
            rzp_order_id=rzp_order['id'],
            amount=registration.registration_fee,
            status='Pending',
            transaction_at=timezone.now(),
        )

        # Render Razorpay payment page
        return render(request, 'payments/razorpay-page.html', {
            'order_id': rzp_order['id'],
            'amount': amount_in_paise,
            'client_id': settings.RZP_CLIENT_ID,
            'uuid': uuid,
            'registration': registration,
        })

@method_decorator(csrf_exempt, name='dispatch')
class PaymentVerify(View):
    def post(self, request, *args, **kwargs):
        data = request.POST

        rzp_order_id = data.get('razorpay_order_id')
        rzp_payment_id = data.get('razorpay_payment_id')
        rzp_signature = data.get('razorpay_signature')

        transaction = get_object_or_404(Transactions, rzp_order_id=rzp_order_id)
        payment = transaction.payment

        # Store Razorpay payment details
        transaction.rzp_payment_id = rzp_payment_id
        transaction.rzp_signature = rzp_signature

        # Razorpay client setup
        client = razorpay.Client(auth=(config('RZP_CLIENT_ID'), config('RZP_CLIENT_SECRET')))

        try:
            # Verify payment signature with Razorpay
            client.utility.verify_payment_signature({
                'razorpay_order_id': rzp_order_id,
                'razorpay_payment_id': rzp_payment_id,
                'razorpay_signature': rzp_signature
            })

            # Mark the transaction as successful
            transaction.status = 'Success'
            transaction.transaction_at = timezone.now()
            transaction.save()

            # Mark the payment as successful
            payment.status = 'Success'
            payment.paid_at = timezone.now()
            payment.save()

            return redirect('send-request-success')  # Redirect to a success page or appropriate view

        except razorpay.errors.SignatureVerificationError:
            # Handle failure case
            transaction.status = 'Failed'
            transaction.transaction_at = timezone.now()
            transaction.save()

            return redirect('send-request-success')  # Or failure page
