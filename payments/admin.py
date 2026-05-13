from django.contrib import admin
from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['patient', 'amount', 'method', 'status', 'paid_at', 'created_at']
    list_filter = ['status', 'method']
    search_fields = ['patient__user__first_name', 'transaction_id']
