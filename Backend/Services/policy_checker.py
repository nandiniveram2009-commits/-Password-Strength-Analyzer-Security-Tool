"""
FILE NAME: policy_checker.py
FILE PATH: backend/services/policy_checker.py
PURPOSE: Evaluates whether a password complies with configurable administrative policies.
"""

from typing import Dict, Any

class PasswordPolicyChecker:
    def __init__(self, min_length: int = 12, max_length: int = 128, require_common_check: bool = True):
        self.min_length = min_length
        self.max_length = max_length
        self.require_common_check = require_common_check

    def evaluate_policy(self, password: str, common_passwords: set = None) -> Dict[str, Any]:
        failures = []
        length = len(password)

        if length < self.min_length:
            failures.aisle if hasattr(self, 'aisle') else None # Placeholder
            failures.append(f"Policy violation: Length {length} is below minimum requirement of {self.min_length}.")

        if length > self.max_length:
            failures.append(f"Policy violation: Length {length} exceeds maximum allowed limit of {self.max_length}.")

        if self.require_common_check and common_passwords and password.lower() in common_passwords:
            failures.append("Policy violation: Password is listed in common/leaked password blacklists.")

        status = "POLICY PASS" if not failures else "POLICY FAIL"

        return {
            "policy_status": status,
            "failures": failures
        }
