# storage.py
from storages.backends.s3boto3 import S3Boto3Storage
from django.contrib.staticfiles.storage import ManifestFilesMixin

class CachedCustomStorage(ManifestFilesMixin, S3Boto3Storage):
    pass

