from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model  # Utiliser le modèle User personnalisé
from gestion_patients.models import Patient
from django.contrib.auth.models import Group
import json
from datetime import datetime
import os

class Command(BaseCommand):
    help = 'Loads patient data from a JSON file into the database'

    def handle(self, *args, **options):
        # Chemin relatif par rapport au répertoire racine du projet
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        json_file_path = os.path.join(base_dir, '..', 'patients.json')  # Remonte d'un niveau depuis gestion_patients

        # Vérifier si le fichier existe
        if not os.path.exists(json_file_path):
            self.stdout.write(self.style.ERROR(f'File not found: {json_file_path}'))
            return

        # Créer le groupe Patients s'il n'existe pas
        group_patients, created = Group.objects.get_or_create(name='Patients')
        if created:
            self.stdout.write(self.style.SUCCESS('Created group "Patients"'))

        # Obtenir le modèle User personnalisé
        User = get_user_model()

        with open(json_file_path, 'r', encoding='utf-8') as file:
            patients_data = json.load(file)
            for patient in patients_data:
                # Créer l'utilisateur
                username = f"{patient['prenom'].lower()}.{patient['nom'].lower()}"
                user, created = User.objects.get_or_create(
                    username=username,
                    defaults={
                        'email': f"{patient['prenom'].lower()}.{patient['nom'].lower()}@example.com",
                        'first_name': patient['prenom'],
                        'last_name': patient['nom']
                    }
                )
                if created:
                    user.set_password(patient['password'])  # Utiliser le mot de passe du JSON
                    user.save()
                    user.groups.add(group_patients)  # Ajouter au groupe Patients

                # Créer ou mettre à jour le patient
                Patient.objects.update_or_create(
                    biometric_id=patient['biometric_id'],
                    defaults={
                        'user': user,
                        'nom': patient['nom'],
                        'prenom': patient['prenom'],
                        'date_naissance': datetime.strptime(patient['date_naissance'], '%Y-%m-%d').date(),
                        'adresse': patient['adresse'],
                        'telephone': patient['telephone']
                    }
                )
        self.stdout.write(self.style.SUCCESS('Successfully loaded patient data'))