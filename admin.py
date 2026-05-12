from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Patient, Doctor, Appointment


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'role', 'phone']
    list_filter = ['role', 'is_active']
    fieldsets = UserAdmin.fieldsets + (
        ('Qo\'shimcha', {'fields': ('role', 'phone', 'address', 'date_of_birth')}),
    )


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ['user', 'blood_group', 'emergency_contact', 'emergency_phone']
    search_fields = ['user__first_name', 'user__last_name', 'user__email']


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ['user', 'specialty', 'experience_years', 'consultation_fee', 'is_available']
    list_filter = ['specialty', 'is_available']


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['patient', 'doctor', 'appointment_date', 'status']
    list_filter = ['status']
    search_fields = ['patient__user__first_name', 'doctor__user__first_name']
