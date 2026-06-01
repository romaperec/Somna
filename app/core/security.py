from argon2 import PasswordHasher
from argon2.exceptions import VerificationError


class PasswordSecurityService:
    def __init__(self):
        self._ph = PasswordHasher()

    def hash(self, password: str) -> str:
        return self._ph.hash(password)

    def verify(self, password: str, hashed_password: str) -> bool:
        try:
            return self._ph.verify(password, hashed_password)
        except VerificationError:
            return False


password_service = PasswordSecurityService()
