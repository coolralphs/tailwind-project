"""
Django settings for tailwind project.

Generated by 'django-admin startproject' using Django 5.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""
import os
from pathlib import Path
from decouple import config
import dj_database_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-e8h-yh7a!=)udp7c&yhccn+29($dfw80s)tf)%e!+rgf79@xd='

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=False, cast=bool)

ALLOWED_HOSTS = ['*']

# RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
# if RENDER_EXTERNAL_HOSTNAME:
#     ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'app',
    'bootstrap5',
    'django_countries',
    'django_bootstrap_datetimepicker',
    'django_flatpickr',
    'bootstrap3_datetime',
    'fontawesomefree',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

ROOT_URLCONF = 'tailwind.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'tailwind.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

if DEBUG:
    DATABASES = {       
        'default': {
            "ENGINE": "django.db.backends.postgresql_psycopg2",
            'NAME': 'tailwind',  # Your database name
            'USER': 'rafael',  # Your database user
            'PASSWORD': '#Tailwind956',  # Your database password
            'HOST': 'localhost',  # Usually localhost
            'PORT': '5432',  # Default PostgreSQL port
        }
    }
else:
    DATABASES = {
        'default': dj_database_url.config(
            # Replace this value with your local database's connection string.
            default='postgresql://rafael:#Tailwind956@localhost:5432/tailwind',
            conn_max_age=600
        )
    # 'default': {
    #     # 'ENGINE': 'django.db.backends.sqlite3',
    #     # 'NAME': BASE_DIR / 'db.sqlite3',
    #     "ENGINE": "django.db.backends.postgresql_psycopg2",
    #     'NAME': 'tailwind',  # Your database name
    #     'USER': 'rafael',  # Your database user
    #     'PASSWORD': '#Tailwind956',  # Your database password
    #     'HOST': 'localhost',  # Usually localhost
    #     'PORT': '5432',  # Default PostgreSQL port
    # }
    }


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

# STATIC_URL = 'static/'
STATIC_URL = '/static/'

# This production code might break development mode, so we check whether we're in DEBUG mode
if not DEBUG:
    # Tell Django to copy static assets into a path called `staticfiles` (this is specific to Render)
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
    # Enable the WhiteNoise storage backend, which compresses static files to reduce disk use
    # and renames the files with unique names for each version to support long-term caching
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_URL = '/login/'

USE_L10N = True

TIME_INPUT_FORMATS = ('%I:%M %p',) 

DJANGO_FLATPICKR = {
    # Name of the theme to use
    # More themes: https://flatpickr.js.org/themes/
    "theme_name": "dark",
    #
    # Complete URL of theme CSS file
    # theme_name is ignored if theme_url is provided
    # "theme_url": "https://..",
    #
    # Global HTML attributes for flatpickr <input> element
    # "attrs": {
    #     "class": "my-custom-class",
    #     "placeholder": "Select Date..",
    # },
    #
    # Global options for flatpickr
    # More options: https://flatpickr.js.org/options/
    # Some options are managed by this package e.g mode, dateFormat, altInput
    # "options": {
    #     "locale": "bn",             # locale option can be set here only
    #     "altFormat": "m/d/Y H:i",   # specify date format on the front-end
    # }
    # You can set date and event hook options using JavaScript, usage in README.
    #
    # HTML template to render the flatpickr input
    # Example: https://github.com/monim67/django-flatpickr/blob/2.0.0/dev/myapp/templates/myapp/custom-flatpickr-input.html
    # "template_name": "your-app/custom-flatpickr-input.html",
    #
    # Specify CDN roots. Choose where from static JS/CSS are served.
    # Can be set to localhost (offline setup) or any other preferred CDN.
    # The default values are:
    #    "flatpickr_cdn_url": "https://cdn.jsdelivr.net/npm/flatpickr@4.6.13/dist/",
    #    "app_static_url": "https://cdn.jsdelivr.net/gh/monim67/django-flatpickr@2.0.0/src/django_flatpickr/static/django_flatpickr/",
    #
    # Advanced:
    # If you want to serve static files yourself without CDN (from staticfiles) and
    # you know how to serve django static files on production server (DEBUG=False)
    # Then download and extract https://registry.npmjs.org/flatpickr/-/flatpickr-4.6.13.tgz
    # Copy the dist directory (package/dist) to any of your static directory and rename it to flatpickr
    # and use following options
    #    "flatpickr_cdn_url": "flatpickr/",
    #    "app_static_url": "django_flatpickr/",
}