"""
FILE NAME: hashing_demo.py
FILE PATH: backend/services/hashing_demo.py
PURPOSE: Educational demonstration of secure password hashing (Argon2id) vs encryption.
"""

from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

class PasswordHashingDemo:
    def __init__(self):
        # Argon2id parameters: memory cost, time cost, parallelism
        self.ph = PasswordHasher(
            time_cost=3, 
            memory_cost=65536, 
            parallelism=4
        )

    def hash_password(self, plaintext: str) -> str:
        """
        Hashes a plaintext password using Argon2id with an automatically generated salt.
        """
        return self.ph.hash(plaintext)

    def verify_password(self, password_hash: str, plaintext: str) -> bool:
        """
        Verifies a plaintext password against an existing Argon2id hash.
        Returns True if matched, False otherwise.
        """
        try:
            return self.ph.verify(password_hash, plaintext)
        except VerifyMismatchError:
            return False

# ==========================================
# CONCEPTUAL CLARIFICATION NOTES:
# ==========================================
# 1. Hashing is ONE-WAY: You cannot decrypt a password hash back into plaintext. 
#    Verification works by hashing the user's input with the stored salt and comparing hashes.
# 2. Encryption is TWO-WAY (Reversible): Encryption involves a secret key used to encrypt 
#    data into ciphertext and decrypt it back into plaintext. Passwords should NEVER be encrypted;
#    they must always be hashed.
# ==========================================
