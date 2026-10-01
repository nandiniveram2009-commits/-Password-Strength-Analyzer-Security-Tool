import re
import math
from typing import Dict, Any, List

class PasswordAnalyzer:
    def __init__(self, common_passwords_path: str = "data/common_passwords.txt"):
        self.common_passwords = self._load_common_passwords(common_passwords_path)
        self.keyboard_patterns = [
            "qwertyuiop", "asdfghjkl", "zxcvbnm",
            "1234567890", "qazwsxedcrfvtgbnyhnujmkiolp"
        ]

    def _load_common_passwords(self, path: str) -> set:
        passwords = set()
        try:
            with open(path, "r", encoding="utf-8") as f:
                for line in f:
                    pw = line.strip().lower()
                    if pw:
                        passwords.add(pw)
        except FileNotFoundError:
            # Fallback basic list if file is missing
            passwords = {"password", "123456", "password123", "admin", "welcome", "letmein", "qwerty"}
        return passwords

    def analyze(self, password: str, context: dict = None) -> Dict[str, Any]:
        if not password:
            return {
                "score": 0,
                "classification": "VERY WEAK",
                "findings": ["Password is empty."],
                "suggestions": ["Please enter a valid password to analyze."],
                "metrics": {"length": 0, "entropy": 0.0}
            }

        findings = []
        suggestions = []
        score = 100

        length = len(password)
        has_lower = any(c.islower() for c in password)
        has_upper = any(c.isupper() for c in password)
        has_digit = any(c.isdigit() for c in password)
        has_symbol = any(not c.isalnum() for c in password)
        
        unique_chars = len(set(password))
        unique_ratio = unique_chars / length if length > 0 else 0

        # 1. Length Evaluation & Penalties
        if length < 8:
            score -= 40
            findings.append(f"Very short length ({length} characters).")
            suggestions.append("Increase your password length to at least 12–16 characters.")
        elif length < 12:
            score -= 20
            findings.append(f"Short length ({length} characters).")
            suggestions.append("Consider lengthening your password to 16+ characters for robust security.")
        elif length >= 16:
            score += 10 # Bonus handled via clamping later

        # 2. Common Password Check
        if password.lower() in self.common_passwords:
            score -= 60
            findings.append("Password matches a known common or leaked password pattern.")
            suggestions.append("Your password matches a commonly used password pattern and should not be used.")

        # 3. Character Diversity
        diversity_count = sum([has_lower, has_upper, has_digit, has_symbol])
        if diversity_count < 2:
            score -= 25
            findings.append("Low character diversity (uses restricted character types).")
            suggestions.append("Incorporate a mix of uppercase letters, lowercase letters, numbers, and symbols.")
        
        if unique_ratio < 0.4 and length > 6:
            score -= 15
            findings.append("High character repetition detected.")
            suggestions.append("Avoid repeating the same characters excessively.")

        # 4. Pattern & Sequence Checks
        seq_findings = self._detect_sequences(password)
        if seq_findings:
            score -= 15 * len(seq_findings)
            findings.extend(seq_findings)
            suggestions.append("Remove predictable numeric or alphabetic sequences (e.g., 1234, abcd).")

        kb_findings = self._detect_keyboard_patterns(password)
        if kb_findings:
            score -= 20 * len(kb_findings)
            findings.extend(kb_findings)
            suggestions.append("Avoid standard keyboard walks such as 'qwerty' or 'asdf'.")

        rep_findings = self._detect_repetition(password)
        if rep_findings:
            score -= 20
            findings.extend(rep_findings)
            suggestions.append("Avoid repeating character blocks or patterns.")

        # 5. Personal Context Check (Optional)
        if context:
            ctx_findings = self._check_context(password, context)
            if ctx_findings:
                score -= 25
                findings.extend(ctx_findings)
                suggestions.append("Avoid including personal information such as names or birth years in your password.")

        # 6. Entropy Estimation
        entropy = self._estimate_entropy(password, diversity_count)

        # Normalize score between 0 and 100
        score = max(0, min(100, score))
        classification = self._classify_score(score)

        if not suggestions and score < 80:
            suggestions.append("Consider using a passphrase made of random, unrelated words.")

        return {
            "score": score,
            "classification": classification,
            "findings": findings,
            "suggestions": list(set(suggestions)), # Deduplicate suggestions
            "metrics": {
                "length": length,
                "has_lower": has_lower,
                "has_upper": has_upper,
                "has_digit": has_digit,
                "has_symbol": has_symbol,
                "unique_character_count": unique_chars,
                "unique_character_ratio": round(unique_ratio, 2),
                "entropy_bits": round(entropy, 2)
            }
        }

    def _detect_sequences(self, password: str) -> List[str]:
        findings = []
        sequences = ["0123456789", "9876543210", "abcdefghijklmnopqrstuvwxyz", "zyxwvutsrqponmlkjihgfedcba"]
        pw_lower = password.lower()
        for seq in sequences:
            for i in range(len(seq) - 3):
                sub = seq[i:i+4]
                if sub in pw_lower:
                    findings.append(f"Contains sequential pattern: '{sub}'")
                    break
        return findings

    def _detect_keyboard_patterns(self, password: str) -> List[str]:
        findings = []
        pw_lower = password.lower()
        for kb in self.keyboard_patterns:
            for i in range(len(kb) - 3):
                sub = kb[i:i+4]
                if sub in pw_lower:
                    findings.append(f"Contains keyboard walk pattern: '{sub}'")
                    break
        return findings

    def _detect_repetition(self, password: str) -> List[str]:
        findings = []
        # Check for 3+ repeating identical characters
        if re.search(r(.)\1{2,}, password):
            findings.append("Contains excessive character repetition (e.g., 'aaa').")
        return findings

    def _check_context(self, password: str, context: dict) -> List[str]:
        findings = []
        pw_lower = password.lower()
        for key, val in context.items():
            if val and len(val.strip()) > 2 and val.strip().lower() in pw_lower:
                findings.append(f"Password appears to contain personal information related to '{key}'.")
        return findings

    def _estimate_entropy(self, password: str, diversity_count: int) -> float:
        pool_size = 0
        if any(c.islower() for c in password): pool_size += 26
        if any(c.isupper() for c in password): pool_size += 26
        if any(c.isdigit() for c in password): pool_size += 10
        if any(not c.isalnum() for c in password): pool_size += 32

        if pool_size == 0:
            return 0.0
        
        # Theoretical entropy: L * log2(N)
        return len(password) * math.log2(pool_size)

    def _classify_score(self, score: int) -> str:
        if score <= 20: return "VERY WEAK"
        elif score <= 40: return "WEAK"
        elif score <= 60: return "MODERATE"
        elif score <= 80: return "STRONG"
        else: return "VERY STRONG"
