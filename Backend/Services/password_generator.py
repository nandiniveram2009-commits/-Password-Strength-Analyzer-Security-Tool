import secrets
import string

class PasswordGenerator:
    @staticmethod
    def generate(length: int = 16, use_upper: bool = True, use_lower: bool = True, use_digits: bool = True, use_symbols: bool = True) -> str:
        char_pool = ""
        if use_lower: char_pool += string.ascii_lowercase
        if use_upper: char_pool += string.ascii_uppercase
        if use_digits: char_pool += string.digits
        if use_symbols: char_pool += string.punctuation

        if not char_pool:
            char_pool = string.ascii_letters + string.digits # Fallback

        # Use secrets module for cryptographic randomness
        password = ''.join(secrets.choice(char_pool) for _ in range(max(12, length)))
        return password
