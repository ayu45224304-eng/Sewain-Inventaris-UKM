import base64
import binascii
import hashlib
import hmac
import secrets

ALGORITHM = "pbkdf2_sha256"
ITERATIONS = 600_000
SALT_BYTES = 16
DERIVED_KEY_BYTES = 32
MIN_ITERATIONS = 100_000
MAX_ITERATIONS = 2_000_000
MIN_PASSWORD_LENGTH = 8
MAX_PASSWORD_LENGTH = 128


def _encode(value):
    return base64.b64encode(value).decode("ascii")


def _decode(value):
    return base64.b64decode(value.encode("ascii"), validate=True)


def hash_password(password):
    if not isinstance(password, str):
        raise ValueError("Password harus berupa teks.")
    if not MIN_PASSWORD_LENGTH <= len(password) <= MAX_PASSWORD_LENGTH:
        raise ValueError(
            f"Password harus berisi {MIN_PASSWORD_LENGTH}–{MAX_PASSWORD_LENGTH} karakter."
        )

    salt = secrets.token_bytes(SALT_BYTES)
    derived_key = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        ITERATIONS,
        dklen=DERIVED_KEY_BYTES,
    )
    return "$".join(
        (ALGORITHM, str(ITERATIONS), _encode(salt), _encode(derived_key))
    )


def verify_password(password, stored_hash):
    if not isinstance(password, str) or not isinstance(stored_hash, str):
        return False
    if not MIN_PASSWORD_LENGTH <= len(password) <= MAX_PASSWORD_LENGTH:
        return False

    try:
        algorithm, iterations_text, salt_text, hash_text = stored_hash.split("$")
        iterations = int(iterations_text)
        if algorithm != ALGORITHM or not MIN_ITERATIONS <= iterations <= MAX_ITERATIONS:
            return False
        salt = _decode(salt_text)
        expected_hash = _decode(hash_text)
        if len(salt) != SALT_BYTES or len(expected_hash) != DERIVED_KEY_BYTES:
            return False
        actual_hash = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            salt,
            iterations,
            dklen=DERIVED_KEY_BYTES,
        )
        return hmac.compare_digest(actual_hash, expected_hash)
    except (ValueError, TypeError, binascii.Error):
        return False


def validate_new_password(password, confirmation=None):
    if not isinstance(password, str):
        raise ValueError("Password baru harus berupa teks.")
    if not MIN_PASSWORD_LENGTH <= len(password) <= MAX_PASSWORD_LENGTH:
        raise ValueError(
            f"Password baru harus berisi {MIN_PASSWORD_LENGTH}–{MAX_PASSWORD_LENGTH} karakter."
        )
    if confirmation is not None and password != confirmation:
        raise ValueError("Konfirmasi password tidak cocok.")
