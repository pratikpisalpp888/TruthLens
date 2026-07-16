"""
TruthLens — Encryption Utilities.
"""

import base64
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes

class AESCipher:
    def __init__(self, key: str):
        # Hash the key to ensure it's 32 bytes (256 bits)
        self.key = hashlib.sha256(key.encode()).digest()

    def encrypt(self, plaintext: bytes) -> bytes:
        iv = get_random_bytes(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        padded_data = pad(plaintext, AES.block_size)
        encrypted = cipher.encrypt(padded_data)
        return iv + encrypted

    def decrypt(self, ciphertext: bytes) -> bytes:
        iv = ciphertext[:AES.block_size]
        actual_ciphertext = ciphertext[AES.block_size:]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        decrypted_padded = cipher.decrypt(actual_ciphertext)
        return unpad(decrypted_padded, AES.block_size)

def encrypt_file(file_data: bytes, key: str) -> bytes:
    cipher = AESCipher(key)
    return cipher.encrypt(file_data)

def decrypt_file(file_data: bytes, key: str) -> bytes:
    cipher = AESCipher(key)
    return cipher.decrypt(file_data)

def generate_file_hash(file_data: bytes) -> str:
    import hashlib
    return hashlib.sha256(file_data).hexdigest()
