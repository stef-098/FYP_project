import os
import base64
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import secrets


def generate_key(password):
    salt = secrets.token_bytes(32)  
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,  # Length of the key in bytes
        salt=salt,
        iterations=100000,  # Number of iterations
    )
    key = base64.urlsafe_b64encode(kdf.derive(password))
    return key
