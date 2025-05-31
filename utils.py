import hashlib
from cryptography.fernet import Fernet

# Generate a static Fernet key (you can make this dynamic if needed)
KEY = Fernet.generate_key()
cipher = Fernet(KEY)

def hash_passkey(passkey: str) -> str:
    return hashlib.sha256(passkey.encode()).hexdigest()

def encrypt_data(text: str) -> str:
    return cipher.encrypt(text.encode()).decode()

def decrypt_data(encrypted_text: str) -> str:
    return cipher.decrypt(encrypted_text.encode()).decode()
