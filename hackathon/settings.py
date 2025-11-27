"""
Django settings for hackathon project.
"""

from pathlib import Path
import os
import dj_database_url

# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent

# -------------------------------
# Security
# -------------------------------

SECRET_KEY = os.getenv("SECRET_KEY", "local-secret-key")  
# Render will inject SECRET_KEY automatically

DEBUG = os.getenv("DEBUG", "False") == "True"

ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "").split()
# Example for Render:  syncroomies-backend.onrender.com

# -------------------------------
# Installed Apps
# -------------------------------

INSTALLED_APPS = [
    "daphne",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
     "corsheaders",
    
    "home",
    "chat",
]

# -------------------------------
# Middleware
# -------------------------------

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
]

# -------------------------------
# URL Settings
# -------------------------------

ROOT_URLCONF = "hackathon.urls"

# -------------------------------
# Templates
# -------------------------------

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# -------------------------------
# ASGI + WSGI
# -------------------------------

ASGI_APPLICATION = "hackathon.asgi.application"
WSGI_APPLICATION = "hackathon.wsgi.application"

# -------------------------------
# Database (Render Auto)
# -------------------------------

DATABASES = {
    "default": dj_database_url.config(
        default=os.getenv(
            "DATABASE_URL",
            "postgresql://swastika@localhost:5432/syncroomies"
        ),
        conn_max_age=600,
    )
}

# -------------------------------
# Redis / Channels
# -------------------------------

REDIS_URL = os.getenv("REDIS_URL")

if REDIS_URL:
    CHANNEL_LAYERS = {
        "default": {
            "BACKEND": "channels_redis.core.RedisChannelLayer",
            "CONFIG": {"hosts": [REDIS_URL]},
        }
    }
else:
    CHANNEL_LAYERS = {
        "default": {
            "BACKEND": "channels.layers.InMemoryChannelLayer"
        }
    }

CORS_ALLOW_ALL_ORIGINS = True

CSRF_TRUSTED_ORIGINS = [
    "https://syncroomies-backend.onrender.com",
    "https://syncroomies-frontend.onrender.com",
    "http://localhost:3000",
]


# -------------------------------
# Password Validation
# -------------------------------

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# -------------------------------
# Internationalization
# -------------------------------

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

# -------------------------------
# Static + Media
# -------------------------------

STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    }
}

# -------------------------------
# Default Primary Key
# -------------------------------

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# --- TEMP: auto-migrate during deploy on Render ---
if os.environ.get("RENDER"):
    import django
    django.setup()
    from django.core.management import call_command
    try:
        call_command("migrate", interactive=False)
    except Exception as e:
        print("MIGRATION ERROR:", e)

