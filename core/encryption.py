import os
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

def derive_key(password: str, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    return kdf.derive(password.encode())

def encrypt_data(data: str, key: bytes) -> dict:
    iv = os.urandom(12)
    cipher = Cipher(algorithms.AES(key), modes.GCM(iv))
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(data.encode()) + encryptor.finalize()
    return {
        'ciphertext': ciphertext.hex(),
        'iv': iv.hex(),
        'tag': encryptor.tag.hex()
    }

def decrypt_data(enc_data: dict, key: bytes) -> str:
    iv = bytes.fromhex(enc_data['iv'])
    tag = bytes.fromhex(enc_data['tag'])
    ciphertext = bytes.fromhex(enc_data['ciphertext'])
    cipher = Cipher(algorithms.AES(key), modes.GCM(iv, tag))
    decryptor = cipher.decryptor()
    plaintext = decryptor.update(ciphertext) + decryptor.finalize()
    return plaintext.decode()