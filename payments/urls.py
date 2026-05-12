from django.urls import path
from . import views

urlpatterns = [
    path('payments/', views.PaymentListView.as_view(), name='payment-list'),
    path('payments/create/', views.PaymentCreateView.as_view(), name='payment-create'),
    path('payments/<int:pk>/', views.PaymentDetailView.as_view(), name='payment-detail'),
    path('payments/<int:pk>/confirm/', views.confirm_payment, name='payment-confirm'),
    path('payments/stats/', views.payment_stats, name='payment-stats'),
]
