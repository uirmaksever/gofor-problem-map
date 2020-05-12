from .base import *  # noqa
from .base import env

# GENERAL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = True
# https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
SECRET_KEY = env(
    "DJANGO_SECRET_KEY",
    default="XLos71KDAtV1ewsz4duiBqy4eOVF9aoKaNe6qoYaz8oYa4KXvfmUedUbJUyPi681",
)
# https://docs.djangoproject.com/en/dev/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ["localhost", "0.0.0.0", "127.0.0.1", ".ngrok.io", "192.168.1.5"]

# CACHES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#caches
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "",
    }
}

# EMAIL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#email-backend
EMAIL_BACKEND = env(
    "DJANGO_EMAIL_BACKEND", default="django.core.mail.backends.console.EmailBackend"
)

# django-debug-toolbar
# ------------------------------------------------------------------------------
# https://django-debug-toolbar.readthedocs.io/en/latest/installation.html#prerequisites
INSTALLED_APPS += ["debug_toolbar"]  # noqa F405
# https://django-debug-toolbar.readthedocs.io/en/latest/installation.html#middleware
MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]  # noqa F405
# https://django-debug-toolbar.readthedocs.io/en/latest/configuration.html#debug-toolbar-config
DEBUG_TOOLBAR_CONFIG = {
    "DISABLE_PANELS": ["debug_toolbar.panels.redirects.RedirectsPanel"],
    "SHOW_TEMPLATE_CONTEXT": True,
}
# https://django-debug-toolbar.readthedocs.io/en/latest/installation.html#internal-ips
INTERNAL_IPS = ["127.0.0.1", "10.0.2.2"]


# django-extensions
# ------------------------------------------------------------------------------
# https://django-extensions.readthedocs.io/en/latest/installation_instructions.html#configuration
INSTALLED_APPS += ["django_extensions"]  # noqa F405

# Your stuff...
# ------------------------------------------------------------------------------

# Copied from production by dev. GDAL/collectstatic on heroku does not play well so let's use remote static in local
# Future note to myself: For some reason once you run collectstatic (a management command), .env file is not taken into account
# So I declared necessary environment variables in PyCharm and created a custom collectstatic, and called all those
# envs in local settings. Since due to GDAL issue you deploy staticfiles from local and disable it in heroku
# For your beloved mind health, use whitenoise and heroku in cookiecutter for future projects even if you won't use
# STATIC
# ------------------------

# DJANGO STORAGES AWS
AWS_S3_OBJECT_PARAMETERS = {
    'Expires': 'Thu, 31 Dec 2099 20:00:00 GMT',
    'CacheControl': 'max-age=94608000',
}

AWS_STORAGE_BUCKET_NAME = env("AWS_STORAGE_BUCKET_NAME")
# See envs/local.env
AWS_ACCESS_KEY_ID = env("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = env("AWS_SECRET_ACCESS_KEY")

AWS_S3_REGION_NAME = env("AWS_S3_REGION_NAME")  # e.g. us-east-2

# STATIC_URL = f"https://{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/"

# Tell django-storages the domain to use to refer to static files.
AWS_S3_CUSTOM_DOMAIN = env("AWS_S3_CUSTOM_DOMAIN")
# Tell the staticfiles app to use S3Boto3 storage when writing the collected static files (when
# you run `collectstatic`). For using AWS
# STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
# DEFAULT_FILE_STORAGE = STATICFILES_STORAGE
AWS_LOCATION = "static/"
# Geo Libraries
# Note: To deploy to heroku a project that requires PostGIS, you should include the buildpack "heroku-geo-buildpack"
# written by heroku. By May 2020, the issue is still not clear. Some say geo libraries such as GEOS and GDAL, it is said
# that those are included in default python buildpack but that is not the case. Even if you include, there are problems
# with staticfiles
