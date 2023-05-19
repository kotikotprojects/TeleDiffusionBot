from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
from bot.config import ENCRYPTION_KEY, BARS_APP_ID


fernet = Fernet(
    base64.urlsafe_b64encode(
        PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            iterations=390000,
            salt=BARS_APP_ID.encode()
        ).derive(ENCRYPTION_KEY)
    )
)


def encrypt(s: str) -> bytes | None:
    try:
        return fernet.encrypt(s.encode())
    except TypeError:
        return None


def decrypt(s: bytes) -> str | None:
    try:
        return fernet.decrypt(s).decode()
    except TypeError:
        return None
