
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Patient, Assurance, RendezVous, DossierMedical
from .forms import PatientForm, AssuranceForm, RendezVousForm, DossierMedicalForm,PrescriptionFormSet
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from .models import BonAssurance,ExamenResultat,PatientUser,Prescription
from django.utils import timezone
import uuid
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from django.contrib.auth.decorators import user_passes_test

"""def accueil(request):
         return render(request, 'accueil.html', {})"""


from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Patient

from .forms import PatientForm  # Assurez-vous d'avoir un formulaire

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Patient

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
        'is_assurance_group': is_assurance_group
    }
    return render(request, 'accueil.html', context)

# Ajoutez d'autres vues si nécessaire (par exemple, patient_create)
from django.shortcuts import redirect, get_object_or_404
from .forms import PatientForm

@login_required
def patient_create(request):
    patient = Patient.objects.filter(user=request.user).first()
    if request.method == 'POST':
        if patient:
            form = PatientForm(request.POST, instance=patient)
        else:
            form = PatientForm(request.POST)
            if form.is_valid():
                patient = form.save(commit=False)
                patient.user = request.user
                patient.save()
                return redirect('accueil')
        if form.is_valid():
            form.save()
            return redirect('accueil')
    else:
        if patient:
            form = PatientForm(instance=patient)
        else:
            form = PatientForm()
    return render(request, 'templates/patient_form.html', {'form': form})
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

"""@login_required
def dossier_create(request):
         if request.method == 'POST':
             form = DossierMedicalForm(request.POST)
             if form.is_valid():
                 form.save()
                 return redirect('patient_list')
         else:
             form = DossierMedicalForm()
         return render(request, 'patient_form.html', {'form': form})"""
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
"""@login_required
def bon_assurance_create(request, patient_id):
    patient = get_object_or_404(PatientUser, pk=patient_id)
    if request.method == 'POST':
        BonAssurance.objects.create(
            patient=patient,
            numero_bon=str(uuid.uuid4())[:8],
        )
        return redirect('patient_list')
    return render(request, 'bon_assurance_form.html', {'patient': patient})
"""


@login_required
def bon_assurance_create(request, patient_id):
    patient = get_object_or_404(PatientUser, pk=patient_id)
    if request.method == 'POST':
        bon = BonAssurance.objects.create(
            patient=patient,
            numero_bon=str(uuid.uuid4())[:8],
        )
        # Générer PDF
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="bon_assurance_{bon.numero_bon}.pdf"'  
        p = canvas.Canvas(response, pagesize=letter)
        p.drawString(100, 750, f"Bon d'Assurance: {bon.numero_bon}")
        p.drawString(100, 730, f"Patient: {bon.patient.nom} {bon.patient.prenom}")
        p.drawString(100, 710, f"Date: {bon.date_creation.strftime('%Y-%m-%d')}")
        p.drawString(100, 690, f"Statut: {bon.statut}")
        p.showPage()
        p.save()
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
def patient_dashboard(request):
    return render(request, 'patient_dashboard.html', {'user': request.user})

@login_required
def examen_resultat_list(request):
    resultats = ExamenResultat.objects.all()
    return render(request, 'examen_resultat_list.html', {'resultats': resultats})



from django.contrib.auth.decorators import user_passes_test

def in_assurance_group(user):
    return user.groups.filter(name='Assurance').exists()

@user_passes_test(in_assurance_group)
def patient_verify(request, patient_id):
    patient = get_object_or_404(PatientUser, pk=patient_id)
    return render(request, 'patient_verify.html', {'patient': patient})



def in_assurance_group(user):
    return user.groups.filter(name='Assurance').exists()


@user_passes_test(in_assurance_group)
def bon_assurance_list(request):
    bons = BonAssurance.objects.all().select_related('patient')
    return render(request, 'bon_assurance_list.html', {'bons': bons})