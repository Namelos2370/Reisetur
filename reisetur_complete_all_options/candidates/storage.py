from django.core.files.storage import FileSystemStorage
from django.conf import settings
from cryptography.fernet import Fernet
from io import BytesIO

class EncryptedFileSystemStorage(FileSystemStorage):
    """Encrypt files with Fernet before saving to disk. Decrypt on open()."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        key = getattr(settings, 'FILE_ENCRYPTION_KEY', None)
        if not key:
            # generate a key for dev; in prod, set FILE_ENCRYPTION_KEY in env
            key = Fernet.generate_key()
        if isinstance(key, str):
            key = key.encode()
        self.fernet = Fernet(key)

    def _save(self, name, content):
        # content may be an UploadedFile; read bytes
        data = content.read()
        enc = self.fernet.encrypt(data)
        # wrap in BytesIO
        return super()._save(name, BytesIO(enc))

    def open(self, name, mode='rb'):
        f = super().open(name, mode)
        data = f.read()
        dec = self.fernet.decrypt(data)
        return BytesIO(dec)
