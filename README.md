# 🦷 Application de Gestion - Clinique Dentaire

Bienvenue sur le dépôt de mon application de gestion de clinique dentaire. Ce projet a été développé avec **Django** (Python) pour faciliter l'administration quotidienne d'un cabinet dentaire : suivi des patients, prise de rendez-vous et génération de documents.

🔗 **Démo en ligne :** [https://warren27026.pythonanywhere.com](https://warren27026.pythonanywhere.com)


## 🚀 Fonctionnalités Principales

* **Gestion des Patients** : Création, modification et listage des dossiers patients (Coordonnées, historique).
* **Prise de Rendez-vous** : Planification des consultations avec statuts (Planifié, Terminé, Annulé).
* **Génération de PDF** 📄 : Création automatique d'ordonnances ou de factures via `ReportLab`.
* **Tableau de Bord** : Vue d'ensemble de l'activité du cabinet.
* **Interface Admin** : Administration sécurisée via Django Admin pour gérer toutes les données.

## 🛠️ Technologies Utilisées

* **Backend** : Python 3, Django 5
* **Base de données** : SQLite (Par défaut) / Compatible PostgreSQL
* **Modules clés** :
    * `reportlab` (Génération PDF)
    * `django-widget-tweaks` (Gestion des formulaires)
* **Frontend** : HTML5, CSS3 (Templates Django)

## 💻 Installation en local

Si vous souhaitez lancer le projet sur votre machine :

1.  **Cloner le projet**
    ```bash
    git clone [https://github.com/Warren27026/clinique_dentaire.git](https://github.com/Warren27026/clinique_dentaire.git)
    cd clinique_dentaire
    ```

2.  **Créer un environnement virtuel**
    ```bash
    python -m venv venv
    # Sur Windows :
    venv\Scripts\activate
    # Sur Mac/Linux :
    source venv/bin/activate
    ```

3.  **Installer les dépendances**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Appliquer les migrations (Base de données)**
    ```bash
    python manage.py migrate
    ```

5.  **Créer un compte administrateur**
    ```bash
    python manage.py createsuperuser
    ```

6.  **Lancer le serveur**
    ```bash
    python manage.py runserver
    ```

Accédez ensuite à l'application via : `http://127.0.0.1:8000`

## 📂 Structure du Projet

* `clinique_dentaire/` : Configuration principale du projet.
* `gestion_patients/` : Application gérant la logique métier (Vues, Modèles).
* `templates/` : Fichiers HTML.
* `static/` : Fichiers CSS, Images et JS.

## 👤 Auteur

**Warren27026**
* GitHub : [github.com/Warren27026](https://github.com/Warren27026)

---
*Ce projet a été réalisé dans le cadre d'un portfolio pour démontrer des compétences en développement Fullstack Python/Django.*
