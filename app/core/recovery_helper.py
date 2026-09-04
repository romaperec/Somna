import hashlib
import secrets


class RecoveryTokenHelper:
    @classmethod
    def generate_pair(cls) -> tuple[str, str]:
        raw_token = secrets.token_urlsafe(32)
        token_hash = hashlib.sha256(raw_token.encode("utf-8")).hexdigest()

        return raw_token, token_hash

    @classmethod
    def hash_token(cls, raw_token: str) -> str:
        return hashlib.sha256(raw_token.encode("utf-8")).hexdigest()

recovery_helper = RecoveryTokenHelper()