
from django import forms
from .models import Patient, Assurance, RendezVous, DossierMedical
from django import forms
from .models import Prescription,PatientUser
from django.forms import modelformset_factory

class PatientForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Mot de passe", help_text="Choisissez un mot de passe pour le patient")

    class Meta:
        model = Patient
        fields = ['biometric_id', 'nom', 'prenom', 'date_naissance', 'adresse', 'telephone']

    def save(self, *args, **kwargs):
        patient = super().save(commit=False)
        if self.cleaned_data['password']:
            patient.password = self.cleaned_data['password']  # Passer le mot de passe à save()
        patient.save()
        return patient

class AssuranceForm(forms.ModelForm):
         class Meta:
             model = Assurance
             fields = ['patient', 'numero_assurance', 'compagnie', 'date_expiration']
             widgets = {
                 'date_expiration': forms.DateInput(attrs={'type': 'date'}),
             }

"""class RendezVousForm(forms.ModelForm):
         class Meta:
             model = RendezVous
             fields = ['patient', 'date_rdv', 'medecin', 'motif']
             widgets = {
                 'date_rdv': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
             }

class DossierMedicalForm(forms.ModelForm):
         class Meta:
             model = DossierMedical
             fields = ['patient', 'antecedents', 'traitements', 'prescriptions']
class PrescriptionForm(forms.ModelForm):
    class Meta:
        model = Prescription
        fields = ['medicament', 'posologie', 'duree']  """

"""class PatientUserForm(forms.ModelForm):
    class Meta:
        model = PatientUser
        fields = ['username', 'nom', 'prenom', 'date_naissance', 'adresse', 'telephone', 'biometric_id']

class DossierMedicalForm(forms.ModelForm):
    class Meta:
        model = DossierMedical
        fields = ['patient', 'antecedents', 'traitements', 'prescriptions']

class RendezVousForm(forms.ModelForm):
    class Meta:
        model = RendezVous
        fields = ['patient', 'date_rdv', 'medecin', 'motif']"""

class PatientUserForm(forms.ModelForm):
    class Meta:
        model = PatientUser
        fields = ['username', 'nom', 'prenom', 'email', 'date_naissance', 'adresse', 'telephone', 'biometric_id']
        widgets = {
            'date_naissance': forms.DateInput(attrs={'type': 'date'}),
        }

class DossierMedicalForm(forms.ModelForm):
    class Meta:
        model = DossierMedical
        fields = ['patient', 'antecedents', 'traitements', 'prescriptions']

class RendezVousForm(forms.ModelForm):
    class Meta:
        model = RendezVous
        fields = ['patient', 'date_rdv', 'medecin', 'motif']
        widgets = {
            'date_rdv': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

PrescriptionFormSet = modelformset_factory(Prescription, fields=('medicament', 'posologie', 'duree'), extra=1)