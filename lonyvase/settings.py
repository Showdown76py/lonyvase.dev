import os
import secrets
from pathlib import Path

from django.utils.translation import gettext_lazy as _

BASE_DIR = Path(__file__).resolve().parent.parent


def _secret_key():
    if key := os.environ.get("DJANGO_SECRET_KEY"):
        return key
    path = BASE_DIR / ".secret_key"
    if not path.exists():
        path.write_text(secrets.token_urlsafe(50))
    return path.read_text().strip()


SECRET_KEY = _secret_key()
DEBUG = os.environ.get("DJANGO_DEBUG", "0") == "1"

CANONICAL_HOST = "lonyvase.dev"
ALLOWED_HOSTS = [CANONICAL_HOST, f"www.{CANONICAL_HOST}", "localhost", "127.0.0.1"]
ALLOWED_HOSTS += [h for h in os.environ.get("DJANGO_EXTRA_HOSTS", "").split(",") if h]

INSTALLED_APPS = [
    "django.contrib.staticfiles",
    "portfolio",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "lonyvase.middleware.CanonicalHostMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "lonyvase.urls"
WSGI_APPLICATION = "lonyvase.wsgi.application"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.template.context_processors.i18n",
                "portfolio.context_processors.site",
            ],
        },
    },
]

DATABASES = {}

LANGUAGE_CODE = "en"
LANGUAGES = [("en", _("English")), ("fr", _("French"))]
LOCALE_PATHS = [BASE_DIR / "locale"]
USE_I18N = True
TIME_ZONE = "Europe/Paris"
USE_TZ = True

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STORAGES = {
    "staticfiles": {"BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage"},
}
if DEBUG:
    STORAGES["staticfiles"] = {"BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"}

SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_REFERRER_POLICY = "strict-origin-when-cross-origin"
X_FRAME_OPTIONS = "DENY"
