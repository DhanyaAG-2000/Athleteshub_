from django.urls import path

from . import views

urlpatterns =[

    path('razorpay/<uuid:uuid>/', views.RazorpayView.as_view(), name='razorpay'), 
    path('verify/', views.PaymentVerify.as_view(), name='payment-verify'),
    path('payments/details/<uuid:uuid>/', views.PaymentDetailView.as_view(), name='payment-details'),  
    path('payments/', views.PaymentListView.as_view(), name='payment-list'),
    path('transaction/',  views.CombinedPaymentTransactionView.as_view(), name='transaction-list'),


]