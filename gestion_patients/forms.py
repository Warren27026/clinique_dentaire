
from django import forms
from .models import Patient, Assurance, RendezVous, DossierMedical,ExamenResultat
from django import forms
from .models import Prescription,PatientUser,ProForma
from django.forms import modelformset_factory
from django.utils import timezone
from django.db import models

from .models import DossierMedical

class PatientForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Mot de passe", help_text="Choisissez un mot de passe pour le patient")
    
    class Meta:
        model = Patient
        fields = ['biometric_id', 'nom', 'prenom', 'date_naissance', 'adresse', 'telephone']

    def save(self, *args, **kwargs):
        patient = super().save(commit=False)
        if self.cleaned_data.get('password'):
            patient.password = self.cleaned_data['password']
        patient.save()

        # Créer un dossier associé si ce n'est pas déjà fait
        if not hasattr(patient, 'dossiermedical'):
            DossierMedical.objects.create(patient=patient)
        
        return patient

class AssuranceForm(forms.ModelForm):
         class Meta:
             model = Assurance
             fields = ['patient', 'numero_assurance', 'compagnie', 'date_expiration']
             widgets = {
                 'date_expiration': forms.DateInput(attrs={'type': 'date'}),
             }



class PatientUserForm(forms.ModelForm):
    class Meta:
        model = PatientUser
        fields = ['username', 'nom', 'prenom', 'email', 'date_naissance', 'adresse', 'telephone', 'biometric_id']
        widgets = {
            'date_naissance': forms.DateInput(attrs={'type': 'date'}),
        }

class DossierMedicalForm(forms.ModelForm):
    patient = forms.ModelChoiceField(
        queryset=Patient.objects.all(),
        label="Patient",
        widget=forms.Select(attrs={'class': 'form-control'}),
    )

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

class ExamenResultatForm(forms.ModelForm):
    class Meta:
        model = ExamenResultat
        fields = ['patient', 'date_examen', 'type_examen', 'resultat']
        widgets = {
            'patient': forms.Select(attrs={'class': 'form-select'}),
            'date_examen': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'type_examen': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex : Radiographie, Scanner...'}),
            'resultat': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Détails du résultat...'}),
        }

class ProFormaForm(forms.ModelForm):
    class Meta:
        model = ProForma
        fields = ['patient', 'statut']  
        widgets = {
            'statut': forms.Select(attrs={'class': 'form-control'}),
            'patient': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'patient': 'Patient',
            'statut': 'Statut',
        }

    def date_creation_display(self):
        date_valeur = self.instance.date_creation
        if date_valeur:
            return date_valeur.strftime('%d/%m/%Y')
        return ''
