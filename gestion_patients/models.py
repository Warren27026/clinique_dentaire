from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from datetime import datetime
from django.conf import settings  
from django.contrib.auth.models import Group
from django.utils import timezone

from django.contrib.auth import get_user_model
class Patient(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    biometric_id = models.CharField(max_length=100, unique=True)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    date_naissance = models.DateField()
    adresse = models.TextField()
    telephone = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.nom} {self.prenom}"

    def save(self, *args, **kwargs):
        if not self.user and hasattr(self, 'password'):
            User = get_user_model()
            username = f"{self.prenom.lower()}.{self.nom.lower()}"
            try:
                user, created = User.objects.get_or_create(
                    username=username,
                    defaults={
                        'email': f"{self.prenom.lower()}.{self.nom.lower()}@example.com",
                        'first_name': self.prenom,
                        'last_name': self.nom
                    }
                )
                if created:  # Seulement si l'utilisateur est nouveau
                    user.set_password(self.password)
                    user.save()
                    group_patients, _ = Group.objects.get_or_create(name='Patients')
                    user.groups.add(group_patients)
                self.user = user
            except Exception as e:
                raise Exception(f"Erreur lors de la création de l'utilisateur : {str(e)}")
        super().save(*args, **kwargs)

class Assurance(models.Model):
       patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
       numero_assurance = models.CharField(max_length=100, unique=True)
       compagnie = models.CharField(max_length=100)
       date_expiration = models.DateField()

       def __str__(self):
           return f"{self.compagnie} - {self.patient}"

class RendezVous(models.Model):
       patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
       date_rdv = models.DateTimeField()
       medecin = models.CharField(max_length=100)
       motif = models.TextField()

       def __str__(self):
           return f"{self.patient} - {self.date_rdv}"

class DossierMedical(models.Model):
       patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
       antecedents = models.TextField()
       traitements = models.TextField()
       prescriptions = models.TextField()
       date_creation = models.DateTimeField(auto_now_add=True)

       def __str__(self):
           return f"Dossier de {self.patient}"
       
class PatientUser(AbstractUser):
    biometric_id = models.CharField(max_length=50, unique=True, blank=True, null=True)  # Champ facultatif
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    date_naissance = models.DateField(blank=True, null=True)  # Rendu facultatif
    adresse = models.TextField()
    telephone = models.CharField(max_length=15)

    REQUIRED_FIELDS = ['nom', 'prenom', 'email']  # Champs requis pour createsuperuser

    def __str__(self):
        return f"{self.nom} {self.prenom}"
    
class BonAssurance(models.Model):
    patient = models.ForeignKey(PatientUser, on_delete=models.CASCADE)
    numero_bon = models.CharField(max_length=50, unique=True)
    statut = models.CharField(max_length=20, choices=[('en_attente', 'En attente'), ('valide', 'Valide')])
    date_creation=datetime.now()

class ProForma(models.Model):
    patient = models.ForeignKey(PatientUser, on_delete=models.CASCADE)
    statut = models.CharField(
        max_length=50,
        choices=[
            ('brouillon', 'Brouillon'),
            ('valide', 'Validé'),
            ('rejeté', 'Rejeté'),
            ('payé', 'Payé'),
        ],
        default='brouillon',
    )
    date_creation = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"ProForma {self.id} - {self.client}"
class ExamenResultat(models.Model):
    patient = models.ForeignKey('gestion_patients.PatientUser', on_delete=models.CASCADE)
    date_examen = models.DateTimeField()
    type_examen = models.CharField(max_length=100)
    resultat = models.TextField()

    def __str__(self):
        return f"{self.type_examen} - {self.patient}"

class Prescription(models.Model):
    dossier = models.ForeignKey('DossierMedical', on_delete=models.CASCADE)
    medicament = models.CharField(max_length=100)
    posologie = models.CharField(max_length=100)
    duree = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.medicament} - {self.dossier}"