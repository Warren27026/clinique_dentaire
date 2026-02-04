
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Patient, Assurance, RendezVous, DossierMedical,ProForma
from .forms import ProFormaForm,ExamenResultatForm,PatientUserForm,PatientForm, AssuranceForm, RendezVousForm, DossierMedicalForm,PrescriptionFormSet
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from .models import BonAssurance,ExamenResultat,PatientUser,Prescription
from django.utils import timezone
import uuid
from django.views.generic import DeleteView
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from django.contrib.auth.decorators import user_passes_test
from datetime import datetime
from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy
from django.contrib import messages
from django.http import HttpResponseForbidden
from functools import wraps
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from io import BytesIO
import os





@login_required
def accueil(request):
    patient = None
    is_patients_group = request.user.groups.filter(name='Patients').exists()
    is_assurance_group = request.user.groups.filter(name='Assurance').exists()
    if request.user.is_authenticated:
        patient = Patient.objects.filter(user=request.user).first()
    context = {
        'patient': patient,
        'patient_count': Patient.objects.count() if patient else 0,
        'appointment_count': 0,
        'is_patients_group': is_patients_group,
        'is_assurance_group': is_assurance_group,
        'current_time': datetime.now().strftime('%H:%M:%S')
    }
    return render(request, 'accueil.html', context)



@login_required
def patient_create(request):
    if request.method == 'POST':
        form = PatientUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(request.POST['password'])  
            user.save()
            add_user_to_group(user, 'Patients')
            return redirect('patient_list')
    else:
        form = PatientUserForm()
    return render(request, 'patient_form.html', {'form': form})

@login_required
def patient_list(request):
         patients = Patient.objects.all()
         return render(request, 'patient_list.html', {'patients': patients})

@login_required
def patient_create(request):
         if request.method == 'POST':
             form = PatientForm(request.POST)
             if form.is_valid():
                 form.save()
                 return redirect('patient_list')
         else:
             form = PatientForm()
         return render(request, 'patient_form.html', {'form': form})

@login_required
def rdv_create(request):
         if request.method == 'POST':
             form = RendezVousForm(request.POST)
             if form.is_valid():
                 form.save()
                 return redirect('patient_list')
         else:
             form = RendezVousForm()
         return render(request, 'appointment_form.html', {'form': form})


@login_required
def dossier_create(request):
    if request.method == 'POST':
        form = DossierMedicalForm(request.POST)
        formset = PrescriptionFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            dossier = form.save()
            for prescription_form in formset:
                if prescription_form.cleaned_data:
                    prescription = prescription_form.save(commit=False)
                    prescription.dossier = dossier
                    prescription.save()
            return redirect('patient_list')
    else:
        form = DossierMedicalForm()
        formset = PrescriptionFormSet(queryset=Prescription.objects.none())
    return render(request, 'dossier_form.html', {'form': form, 'formset': formset})
@login_required
def patient_edit(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    if request.method == 'POST':
        form = PatientForm(request.POST, instance=patient)
        if form.is_valid():
            form.save()
            return redirect('patient_list')
    else:
        form = PatientForm(instance=patient)
    return render(request, 'patient_form.html', {'form': form})
def patient_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('patient_dashboard')
        else:
            return render(request, 'patient_login.html', {'error': 'Identifiants invalides'})
    return render(request, 'patient_login.html')




@login_required
def bon_assurance_create(request, patient_id):
    patient = get_object_or_404(PatientUser, pk=patient_id)

    if request.method == 'POST':
        bon = BonAssurance.objects.create(
            patient=patient,
            numero_bon=str(uuid.uuid4())[:8],
        )

        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter,
                                rightMargin=40, leftMargin=40,
                                topMargin=60, bottomMargin=40)

        styles = getSampleStyleSheet()
        elements = []

        # Titre principal
        title_style = styles['Title']
        title = Paragraph("Bon d'Assurance", title_style)
        elements.append(title)
        elements.append(Spacer(1, 20))

        # Infos du bon sous forme de tableau
        data = [
            ['Numéro du Bon:', bon.numero_bon],
            ['Patient:', f"{bon.patient.nom} {bon.patient.prenom}"],
            ['Date de création:', bon.date_creation.strftime('%Y-%m-%d')],
            ['Statut:', bon.statut],
        ]

        table = Table(data, colWidths=[150, 300])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 12),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ]))
        elements.append(table)
        elements.append(Spacer(1, 30))

        # Message ou info supplémentaire
        footer = Paragraph("Merci de conserver ce bon d'assurance pour vos démarches administratives.", styles['Normal'])
        elements.append(footer)

        doc.build(elements)

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="bon_assurance_{bon.numero_bon}.pdf"'
        response.write(buffer.getvalue())
        buffer.close()

        return response

    return render(request, 'bon_assurance_form.html', {'patient': patient})

@login_required
def bon_assurance_validate(request, bon_id):
    bon = get_object_or_404(BonAssurance, pk=bon_id)
    if request.method == 'POST':
        statut = request.POST.get('statut')
        if statut in ['valide', 'rejeté']:
            bon.statut = statut
            bon.save()
            return redirect('patient_list')  
    return render(request, 'bon_assurance_validate.html', {'bon': bon})
@login_required
def appointment_list(request):
    appointments = RendezVous.objects.all()
    return render(request, 'appointment_list.html', {'appointments': appointments})
@login_required
def examen_resultat_list(request):
    resultats = ExamenResultat.objects.all()
    return render(request, 'examen_resultat_list.html', {'resultats': resultats})


@login_required

def patient_verify(request, patient_id):
    patient = get_object_or_404(PatientUser, pk=patient_id)
    return render(request, 'patient_verify.html', {'patient': patient})
@login_required
@login_required
def patient_dashboard(request):
    user = request.user
    # Récupérer les rendez-vous du patient
    rendez_vous = RendezVous.objects.filter(patient=user).order_by('date')
    # Récupérer le dossier médical du patient (supposons un seul dossier par patient)
    dossier = DossierMedical.objects.filter(patient=user).first()

    context = {
        'rendez_vous': rendez_vous,
        'dossier': dossier,
    }
    return render(request, 'patient_dashboard.html', context)


@login_required
def examen_resultat_list(request):
    resultats = ExamenResultat.objects.all()
    return render(request, 'examen_resultat_list.html', {'resultats': resultats})



from django.contrib.auth.decorators import user_passes_test

def in_assurance_group(user):
    return user.groups.filter(name='Assurance').exists()

@login_required
def patient_verify(request, patient_id):
    patient = get_object_or_404(PatientUser, pk=patient_id)
    return render(request, 'patient_verify.html', {'patient': patient})



def in_assurance_group(user):
    return user.groups.filter(name='Assurance').exists()


@login_required
def bon_assurance_list(request):
    bons = BonAssurance.objects.all().select_related('patient')
    return render(request, 'bon_assurance_list.html', {'bons': bons})


from django.contrib.auth.models import Group
@login_required
def add_user_to_group(user, group_name):
    group, created = Group.objects.get_or_create(name=group_name)
    user.groups.add(group)
    user.save()
@login_required
def consulter_dossier(request):
    dossiers = DossierMedical.objects.filter(patient__user=request.user)
    return render(request, 'dossier_patient.html', {'dossiers': dossiers})

@login_required
def gerer_rdv(request):
    rdvs = RendezVous.objects.filter(patient__user=request.user)
    return render(request, 'rdv_patient.html', {'rdvs': rdvs})
@login_required
def enregistrer_patient(request):
    if request.method == 'POST':
        form = PatientUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(request.POST['password'])
            user.save()
            add_user_to_group(user, 'Patients')
            return redirect('patient_list')
    else:
        form = PatientUserForm()
    return render(request, 'enregistrer_patient.html', {'form': form})


@login_required
def gerer_dossier_medical(request, patient_id):
    patient = get_object_or_404(PatientUser, pk=patient_id)
    if request.method == 'POST':
        form = DossierMedicalForm(request.POST)
        if form.is_valid():
            dossier = form.save(commit=False)
            dossier.patient = patient
            dossier.save()
            return redirect('dossier_list')
    else:
        form = DossierMedicalForm()
    return render(request, 'dossier_form.html', {'form': form, 'patient': patient})

@login_required
def consulter_bons_assurance(request):
    bons = BonAssurance.objects.all()
    return render(request, 'bons_assurance_list.html', {'bons': bons})
@login_required
def valider_proforma(request, proforma_id):
    proforma = get_object_or_404(ProForma, pk=proforma_id)
    if request.method == 'POST':
        statut = request.POST.get('statut')
        if statut in ['valide', 'rejeté']:
            proforma.statut = statut
            proforma.save()
            messages.success(request, f"Proforma {statut} avec succès.")
        else:
            messages.error(request, "Statut invalide.")
        return redirect('proforma_list')
    return render(request, 'valider_proforma.html', {'proforma': proforma})
@login_required
def proforma_list(request):
    proformas = ProForma.objects.all()
    return render(request, 'proforma_list.html', {'proformas': proformas})

@login_required
def modifier_examen_resultat(request, pk):
    resultat = get_object_or_404(ExamenResultat, pk=pk)
    if request.method == "POST":
        form = ExamenResultatForm(request.POST, instance=resultat)
        if form.is_valid():
            form.save()
            return redirect('examen_resultat_list')  
    else:
        form = ExamenResultatForm(instance=resultat)
    return render(request, 'modifier_examen_resultat.html', {'form': form})
@login_required
def delete_resultat(request, pk):
    resultat = get_object_or_404(ExamenResultat, pk=pk)
    if request.method == "POST":
        resultat.delete()
        return redirect('examen_resultat_list')  
    return render(request, 'supprimer_examen_resultat.html', {'resultat': resultat})

@login_required
def edit_resultat(request, pk):
    resultat = get_object_or_404(ExamenResultat, pk=pk)
    if request.method == 'POST':
        form = ExamenResultatForm(request.POST, instance=resultat)
        if form.is_valid():
            form.save()
            return redirect('examen_resultat_list')  # Redirection après la modification
    else:
        form = ExamenResultatForm(instance=resultat)
    return render(request, 'edit_resultat.html', {'form': form})
@login_required
def dossier_patient(request):
    dossiers = DossierMedical.objects.all()  # Récupère tous les dossiers médicaux
    return render(request, 'dossier_patient.html', {'dossiers': dossiers})

class DossierEditView(UpdateView):
    model = DossierMedical
    fields = ['patient', 'antecedents', 'traitements', 'prescriptions']
    template_name = 'dossier_edit.html'
    success_url = reverse_lazy('dossier_patient')




@login_required
def rdv_edit(request, pk):
    rdv = get_object_or_404(RendezVous, pk=pk)
    if request.method == "POST":
        form = RendezVousForm(request.POST, instance=rdv)
        if form.is_valid():
            form.save()
            return redirect('appointment_list')  # Redirection vers la liste des rendez-vous
    else:
        form = RendezVousForm(instance=rdv)
    return render(request, 'appointment_form.html', {'form': form})

@login_required
def delete_appointment(request, pk):
    appointment = get_object_or_404(RendezVous, pk=pk)
    appointment.delete()
    messages.success(request, "Le rendez-vous a été supprimé avec succès.")
    return redirect('appointment_list')

@login_required
def dossier_form(request):
    return render(request, 'dossier_form.html')


class PatientDeleteView(DeleteView):
    model = Patient
    template_name = 'patient_confirm_delete.html'
    success_url = reverse_lazy('patient_list')

@login_required
def proforma_list(request):
    proformas = ProForma.objects.all()
    return render(request, 'proforma_list.html', {'proformas': proformas})


@login_required
def proforma_create(request):
    if request.method == "POST":
        form = ProFormaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('proforma_list')
    else:
        form = ProFormaForm()
    return render(request, 'proforma_form.html', {'form': form})
@login_required
def proforma_edit(request, pk):
    proforma = get_object_or_404(ProForma, pk=pk)
    if request.method == "POST":
        form = ProFormaForm(request.POST, instance=proforma)
        if form.is_valid():
            form.save()
            return redirect('proforma_list')
    else:
        form = ProFormaForm(instance=proforma)
    return render(request, 'proforma_form.html', {'form': form})
@login_required
def proforma_delete(request, pk):
    proforma = get_object_or_404(ProForma, pk=pk)
    if request.method == "POST":
        proforma.delete()
        return redirect('proforma_list')
    return render(request, 'proforma_confirm_delete.html', {'proforma': proforma})

@login_required
def create_resultat(request):
    if request.method == 'POST':
        form = ExamenResultatForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('examen_resultat_list')  # redirection après création
    else:
        form = ExamenResultatForm()
    return render(request, 'create_resultat.html', {'form': form})
@login_required
def create_resultat(request):
    if request.method == 'POST':
        form = ExamenResultatForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('examen_resultat_list')  # redirection après création
    else:
        form = ExamenResultatForm()
    return render(request, 'create_resultat.html', {'form': form})



@login_required
def dossier_create(request):
    if request.method == 'POST':
        form = DossierMedicalForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dossier_patient')  # redirige vers la liste après création
    else:
        form = DossierMedicalForm()
    return render(request, 'dossier_form.html', {'form': form})
@login_required
def dossier_delete(request, pk):
    dossier = get_object_or_404(DossierMedical, pk=pk)
    if request.method == "POST":
        dossier.delete()
        messages.success(request, "Le dossier a été supprimé avec succès.")
        return redirect('dossier_patient')  
    return render(request, 'dossier_confirm_delete.html', {'dossier': dossier})


