from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .models import User, Patient, Doctor, Appointment
from .serializers import (
    UserRegisterSerializer, UserSerializer,
    PatientSerializer, DoctorSerializer, AppointmentSerializer
)


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            'message': 'Muvaffaqiyatli ro\'yxatdan o\'tdingiz!',
            'user': UserSerializer(user).data,
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        }, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)
    if user:
        refresh = RefreshToken.for_user(user)
        return Response({
            'message': 'Muvaffaqiyatli kirdingiz!',
            'user': UserSerializer(user).data,
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        })
    return Response({'error': 'Username yoki parol noto\'g\'ri!'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def profile_view(request):
    return Response(UserSerializer(request.user).data)


class PatientListView(generics.ListAPIView):
    queryset = Patient.objects.select_related('user').all()
    serializer_class = PatientSerializer
    permission_classes = [permissions.IsAdminUser]


class PatientDetailView(generics.RetrieveUpdateAPIView):
    queryset = Patient.objects.select_related('user').all()
    serializer_class = PatientSerializer
    permission_classes = [permissions.IsAuthenticated]


class DoctorListView(generics.ListAPIView):
    queryset = Doctor.objects.filter(is_available=True).select_related('user')
    serializer_class = DoctorSerializer
    permission_classes = [permissions.AllowAny]


class DoctorDetailView(generics.RetrieveAPIView):
    queryset = Doctor.objects.select_related('user').all()
    serializer_class = DoctorSerializer
    permission_classes = [permissions.AllowAny]


class AppointmentListCreateView(generics.ListCreateAPIView):
    serializer_class = AppointmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            return Appointment.objects.all()
        elif user.role == 'doctor':
            return Appointment.objects.filter(doctor__user=user)
        else:
            return Appointment.objects.filter(patient__user=user)

    def perform_create(self, serializer):
        patient = self.request.user.patient_profile
        serializer.save(patient=patient)


class AppointmentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [permissions.IsAuthenticated]
