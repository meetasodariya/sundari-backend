"""
Django settings for Sundari Silk Palace Backend.

Configured for:
  - Neon PostgreSQL (free, scale-to-zero, IPv4-compatible)
  - Cloudinary (media/image storage)
  - Render (backend hosting)
  - Vercel (Next.js frontend, CORS-allowed)
  - WhiteNoise (static files on Render)
"""

import os
from pathlib import Path
import dj_database_url
from dotenv import load_dotenv

# ---------------------------------------------------------------------------
# Base Setup
# ---------------------------------------------------------------------------

# Load .env file when running locally (Render sets vars via dashboard)
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

# ---------------------------------------------------------------------------
# Security
# ---------------------------------------------------------------------------

SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-change-me-in-production')

# SECURITY: Always False in production (set DEBUG=True only in local .env)
DEBUG = os.getenv('DEBUG', 'False').lower() in ('true', '1', 't')

# Render provides the host via RENDER_EXTERNAL_HOSTNAME env var automatically
ALLOWED_HOSTS = ['localhost', '127.0.0.1']

RENDER_EXTERNAL_HOSTNAME = os.getenv('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)

# Also allow any extra hosts from env (comma-separated)
EXTRA_ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '')
if EXTRA_ALLOWED_HOSTS:
    ALLOWED_HOSTS.extend([h.strip() for h in EXTRA_ALLOWED_HOSTS.split(',') if h.strip()])

# Trust Render's reverse proxy for HTTPS
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# ---------------------------------------------------------------------------
# Application Definition
# ---------------------------------------------------------------------------

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',

    # Cloudinary Storage MUST come before django.contrib.staticfiles
    'cloudinary_storage',
    'django.contrib.staticfiles',
    'cloudinary',

    # Third-Party
    'rest_framework',
    'corsheaders',

    # Local
    'store',
]

MIDDLEWARE = [
    # CORS must be first
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    # WhiteNoise serves static files — placed right after SecurityMiddleware
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# ---------------------------------------------------------------------------
# Database — Neon PostgreSQL (free, scale-to-zero, true IPv4)
# ---------------------------------------------------------------------------
# Local: uses SQLite (no DATABASE_URL in .env)
# Production: uses Neon via DATABASE_URL env var (set in Render dashboard)
#
# Neon connection string format:
#   postgresql://user:password@ep-xxx-xxx.ap-south-1.aws.neon.tech/neondb?sslmode=require
#
# conn_health_checks=True is CRITICAL for Neon's scale-to-zero:
#   it validates the connection before use so stale connections after
#   Neon's compute has slept are transparently recycled.

DATABASE_URL = os.getenv('DATABASE_URL')

if DATABASE_URL:
    DATABASES = {
        'default': dj_database_url.config(
            default=DATABASE_URL,
            conn_max_age=600,        # Keep connections alive for 10 min
            conn_health_checks=True, # Re-validate connections after Neon sleep
            ssl_require=True,        # Neon always requires SSL
        )
    }
else:
    # Local development fallback — SQLite (no setup needed)
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# ---------------------------------------------------------------------------
# Password Validation
# ---------------------------------------------------------------------------

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ---------------------------------------------------------------------------
# Internationalisation — India Standard Time
# ---------------------------------------------------------------------------

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'
USE_I18N = True
USE_TZ = True

# ---------------------------------------------------------------------------
# Static Files — WhiteNoise (Render)
# ---------------------------------------------------------------------------

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# ---------------------------------------------------------------------------
# Media / Cloudinary Configuration
# ---------------------------------------------------------------------------

CLOUDINARY_STORAGE = {
    'CLOUD_NAME': os.getenv('CLOUDINARY_CLOUD_NAME', ''),
    'API_KEY': os.getenv('CLOUDINARY_API_KEY', ''),
    'API_SECRET': os.getenv('CLOUDINARY_API_SECRET', ''),
}

# STORAGES dict is the Django 4.2+ unified storage config.
# We use Cloudinary for media (product images) and WhiteNoise for static.
STORAGES = {
    "default": {
        # Use Cloudinary if configured, else fall back to local filesystem (dev)
        "BACKEND": (
            "cloudinary_storage.storage.MediaCloudinaryStorage"
            if os.getenv('CLOUDINARY_CLOUD_NAME')
            else "django.core.files.storage.FileSystemStorage"
        ),
    },
    "staticfiles": {
        # WhiteNoise compressed+cached storage for Render
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# ---------------------------------------------------------------------------
# CORS — Allow Next.js frontend to call this API
# ---------------------------------------------------------------------------

CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000',
    'http://127.0.0.1:3000',
    # Production Vercel deployment
    'https://sundari-silk-palace.vercel.app',
]

# Allow any custom frontend URL set in env (e.g. preview deployments)
FRONTEND_URL = os.getenv('FRONTEND_URL', '')
if FRONTEND_URL and FRONTEND_URL not in CORS_ALLOWED_ORIGINS:
    CORS_ALLOWED_ORIGINS.append(FRONTEND_URL)

# Allow Vercel preview URLs (*.vercel.app)
CORS_ALLOWED_ORIGIN_REGEXES = [
    r"^https://sundari-silk-palace.*\.vercel\.app$",
]

CORS_ALLOW_CREDENTIALS = True

# ---------------------------------------------------------------------------
# CSRF Trusted Origins (required for Django admin behind Render's HTTPS)
# ---------------------------------------------------------------------------

CSRF_TRUSTED_ORIGINS = [
    'https://sundari-silk-palace.vercel.app',
]
if RENDER_EXTERNAL_HOSTNAME:
    CSRF_TRUSTED_ORIGINS.append(f'https://{RENDER_EXTERNAL_HOSTNAME}')

# ---------------------------------------------------------------------------
# REST Framework
# ---------------------------------------------------------------------------

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
}

# ---------------------------------------------------------------------------
# Misc
# ---------------------------------------------------------------------------

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'