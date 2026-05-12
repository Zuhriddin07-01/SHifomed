from rest_framework import serializers
from .models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source='patient.user.get_full_name', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    method_display = serializers.CharField(source='get_method_display', read_only=True)

    class Meta:
        model = Payment
        fields = '__all__'
        read_only_fields = ['patient', 'paid_at', 'created_at']
