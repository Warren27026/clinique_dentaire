from django.urls import path
from . import views

"""urlpatterns = [
    path('', views.accueil, name='accueil'),
    path('enregistrer_patient/', views.enregistrer_patient, name='enregistrer_patient'),
    path('authentifier_patient/', views.authentifier_patient, name='authentifier_patient'),
    path('gerer_rendez_vous/', views.gerer_rendez_vous, name='gerer_rendez_vous'),
    path('gerer_dossier_medical/', views.gerer_dossier_medical, name='gerer_dossier_medical'),
]"""

from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView
urlpatterns = [
       path('', views.accueil, name='accueil'),
       path('patients/', views.patient_list, name='patient_list'),
       path('patients/create/', views.patient_create, name='patient_create'),
       path('rdv/create/', views.rdv_create, name='rdv_create'),
       path('dossier/create/', views.dossier_create, name='dossier_create'),
       path('patients/edit/<int:pk>/', views.patient_edit, name='patient_edit'),
       path('patient/login/', views.patient_login, name='patient_login'),
       path('patients/<int:patient_id>/bon/create/', views.bon_assurance_create, name='bon_assurance_create'),
       path('bon/<int:bon_id>/validate/', views.bon_assurance_validate, name='bon_assurance_validate'),
       path('appointments/', views.appointment_list, name='appointment_list'),
       path('examens/', views.examen_resultat_list, name='examen_resultat_list'),
       path('patients/<int:patient_id>/verify/', views.patient_verify, name='patient_verify'),
       path('patient/login/', views.patient_login, name='patient_login'),
       path('patient/dashboard/', views.patient_dashboard, name='patient_dashboard'),
       path('bon/', views.bon_assurance_list, name='bon_assurance_list'),
       path('accounts/logout/', LogoutView.as_view(template_name='registration/logged_out.html'), name='logout'),
   ]
