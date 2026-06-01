from argon2 import PasswordHasher


class PasswordSecurityService:
    def __init__(self):
        self._ph = PasswordHasher()

    def hash(self, password: str) -> str:
        return self._ph.hash(password)

    def verify(self, password: str, hashed_password: str) -> bool:
        return self._ph.verify(password, hashed_password)


password_service = PasswordSecurityService()
