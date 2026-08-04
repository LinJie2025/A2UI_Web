"""AES-256 symmetric encryption service using Fernet.

The encryption key is derived from the application SECRET_KEY.
"""

import base64
import hashlib
from cryptography.fernet import Fernet
from app.config import settings


def _derive_fernet_key(secret: str) -> bytes:
    """Derive a 32-byte Fernet key from the application secret."""
    digest = hashlib.sha256(secret.encode()).digest()
    return base64.urlsafe_b64encode(digest)


_fernet = Fernet(_derive_fernet_key(settings.SECRET_KEY))


def encrypt(plaintext: str) -> str:
    """Encrypt a plaintext string and return base64-encoded ciphertext.

    Args:
        plaintext: The string to encrypt.

    Returns:
        Base64-encoded encrypted string.
    """
    if not plaintext:
        return ""
    return _fernet.encrypt(plaintext.encode("utf-8")).decode("utf-8")


def decrypt(ciphertext: str) -> str:
    """Decrypt a base64-encoded ciphertext back to plaintext.

    Args:
        ciphertext: The base64-encoded encrypted string.

    Returns:
        Decrypted plaintext string, or empty string if input is empty.
    """
    if not ciphertext:
        return ""
    return _fernet.decrypt(ciphertext.encode("utf-8")).decode("utf-8")
