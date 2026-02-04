from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import PatientUser, Patient, Assurance, RendezVous, DossierMedical, BonAssurance, ExamenResultat

class CustomUserAdmin(UserAdmin):
    model = PatientUser
    list_display = ('username', 'email', 'nom', 'prenom', 'date_naissance', 'is_staff')
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('biometric_id', 'nom', 'prenom', 'date_naissance', 'adresse', 'telephone')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('biometric_id', 'nom', 'prenom', 'date_naissance', 'adresse', 'telephone')}),
    )

admin.site.register(PatientUser, CustomUserAdmin)
admin.site.register(Patient)
admin.site.register(Assurance)
admin.site.register(RendezVous)
admin.site.register(DossierMedical)
admin.site.register(BonAssurance)
admin.site.register(ExamenResultat)
