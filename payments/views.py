from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.utils import timezone
from .models import Payment
from .serializers import PaymentSerializer


class PaymentListView(generics.ListAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            return Payment.objects.all()
        return Payment.objects.filter(patient__user=user)


class PaymentCreateView(generics.CreateAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        patient = self.request.user.patient_profile
        serializer.save(patient=patient)


class PaymentDetailView(generics.RetrieveAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def confirm_payment(request, pk):
    try:
        payment = Payment.objects.get(pk=pk, patient__user=request.user)
        if payment.status == 'pending':
            payment.status = 'paid'
            payment.paid_at = timezone.now()
            payment.save()
            return Response({
                'message': 'To\'lov muvaffaqiyatli amalga oshirildi!',
                'payment': PaymentSerializer(payment).data
            })
        return Response({'error': 'Bu to\'lov allaqachon qayta ishlangan!'}, status=status.HTTP_400_BAD_REQUEST)
    except Payment.DoesNotExist:
        return Response({'error': 'To\'lov topilmadi!'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def payment_stats(request):
    if request.user.role != 'admin':
        return Response({'error': 'Ruxsat yo\'q!'}, status=status.HTTP_403_FORBIDDEN)
    total = Payment.objects.filter(status='paid').count()
    total_amount = sum(p.amount for p in Payment.objects.filter(status='paid'))
    pending = Payment.objects.filter(status='pending').count()
    return Response({
        'total_paid': total,
        'total_amount': total_amount,
        'pending_payments': pending,
    })
