INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.admin",
    "rest_framework",
    "django_filters",
    "django_project.apps.ProjectConfig",
]

MIDDLEWARE = [
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
]

SECRET_KEY = "*"

ROOT_URLCONF = "django_project.urls"

DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"}}

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "APP_DIRS": True,
        "NAME": "default",
    }
]

REST_FRAMEWORK = {
    "DEFAULT_THROTTLE_CLASSES": ("django_project.api.throttle.ThrottleScope",),
    "DEFAULT_THROTTLE_RATES": {"throttle_scope": "1/min"},
}
