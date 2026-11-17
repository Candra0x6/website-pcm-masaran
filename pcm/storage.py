import os
from pathlib import Path
from django.core.files.storage import FileSystemStorage
from storages.backends.s3boto3 import S3Boto3Storage


class ResilientStorage(FileSystemStorage):
    def __init__(self, *args, **kwargs):
        if os.environ.get('VERCEL'):
            location = Path('/tmp/media')
        else:
            location = kwargs.get('location')
        if location:
            os.makedirs(location, exist_ok=True)
            kwargs['location'] = str(location)
        super().__init__(*args, **kwargs)

    def _save(self, name, content):
        try:
            return super()._save(name, content)
        except (PermissionError, OSError):
            tmp_location = Path('/tmp/media')
            os.makedirs(tmp_location, exist_ok=True)
            self.location = str(tmp_location)
            return super()._save(name, content)


class ResilientS3Storage(S3Boto3Storage):
    def _save(self, name, content):
        try:
            return super()._save(name, content)
        except Exception:
            fallback = ResilientStorage()
            return fallback._save(name, content)

    def url(self, name):
        try:
            return super().url(name)
        except Exception:
            return f"/media/{name}"
