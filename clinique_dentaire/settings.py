import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'votre-cle-secrete-ici'

DEBUG = True

ALLOWED_HOSTS = []

"""INSTALLED_APPS = [
       'django.contrib.admin',
       'django.contrib.auth',
       'django.contrib.contenttypes',
       'django.contrib.sessions',
       'django.contrib.messages',
       'django.contrib.staticfiles',
       'gestion_patients',
   ]"""
INSTALLED_APPS = [
    'gestion_patients.apps.GestionPatientsConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'widget_tweaks',
]

MIDDLEWARE = [
       'django.middleware.security.SecurityMiddleware',
       'django.contrib.sessions.middleware.SessionMiddleware',
       'django.middleware.common.CommonMiddleware',
       'django.middleware.csrf.CsrfViewMiddleware',
       'django.contrib.auth.middleware.AuthenticationMiddleware',
       'django.contrib.messages.middleware.MessageMiddleware',
       'django.middleware.clickjacking.XFrameOptionsMiddleware',
   ]

ROOT_URLCONF = 'clinique_dentaire.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',  # Nécessaire pour l'admin
        'DIRS': [BASE_DIR / 'templates'],  # Répertoire des templates globaux
        'APP_DIRS': True,  # Cherche les templates dans les dossiers des applications
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'libraries': {
                'widget_tweaks': 'widget_tweaks.templatetags.widget_tweaks',  # Pour le filtre add_class
            },
        },
    },
]

WSGI_APPLICATION = 'clinique_dentaire.wsgi.application'

DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.sqlite3',
           'NAME': BASE_DIR / 'db.sqlite3',
       }
   }

AUTH_PASSWORD_VALIDATORS = [
       {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
       {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
       {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
       {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
   ]

LANGUAGE_CODE = 'fr-fr'

TIME_ZONE = 'Africa/Douala'

USE_I18N = True

USE_TZ = True

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_REDIRECT_URL = '/patients/'  # Redirige vers la liste des patients après connexion
#gestion de l'envoi de mail
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'warrenshamir10@gmail.com'
EMAIL_HOST_PASSWORD = 'votre-mot-de-passe'

AUTH_USER_MODEL = 'gestion_patients.PatientUser'
LOGOUT_REDIRECT_URL = '/patient/login/'#ADns kle cas où on veut se déconnecté