"""
DealFlow360 — Authentication primitives.

Deliberately stdlib-only. bcrypt/argon2 wheels need a build toolchain on some
Windows setups and a hackathon cannot afford "it won't install on the demo
laptop", so this uses PBKDF2-HMAC-SHA256 for passwords and a hand-rolled
HS256 JWT. Both are standard constructions, not hand-waved crypto.

Replaces the previous scheme, where the bearer token was literally the user's id
or email and passwords were compared as plaintext.
"""

import base64
import hashlib
import hmac
import json
import os
import secrets
import sys
import time

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

# OWASP's floor for PBKDF2-SHA256 is well above this; 240k is a balance that
# keeps login snappy in a live demo while staying a real work factor.
PBKDF2_ITERATIONS = 240_000
SALT_BYTES = 16

JWT_ALGORITHM = "HS256"
DEFAULT_EXPIRY_MINUTES = int(os.getenv("JWT_EXPIRY_MINUTES", "60"))


def _secret() -> str:
    key = os.getenv("JWT_SECRET") or os.getenv("SECRET_KEY")
    if not key:
        # Never silently fall back to a constant in a deployed setting.
        raise RuntimeError(
            "JWT_SECRET (or SECRET_KEY) is not set. Add it to .env before starting the API."
        )
    return key


# ─────────────────────────────────────────────────────────────────────
# Passwords
# ─────────────────────────────────────────────────────────────────────
def hash_password(password: str) -> str:
    """Return 'pbkdf2_sha256$<iterations>$<salt_b64>$<hash_b64>'."""
    if not password:
        raise ValueError("password must not be empty")
    salt = secrets.token_bytes(SALT_BYTES)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, PBKDF2_ITERATIONS)
    return "$".join([
        "pbkdf2_sha256",
        str(PBKDF2_ITERATIONS),
        base64.b64encode(salt).decode("ascii"),
        base64.b64encode(digest).decode("ascii"),
    ])


def verify_password(password: str, stored: str) -> bool:
    """
    Constant-time verification.

    Accepts a legacy plaintext value so seeded accounts keep working until
    scripts/seed_users.py has rehashed them; anything not in the pbkdf2 format
    is treated as legacy plaintext.
    """
    if not stored:
        return False

    if not stored.startswith("pbkdf2_sha256$"):
        return hmac.compare_digest(str(password), str(stored))

    try:
        _, iterations, salt_b64, hash_b64 = stored.split("$", 3)
        salt = base64.b64decode(salt_b64)
        expected = base64.b64decode(hash_b64)
        candidate = hashlib.pbkdf2_hmac(
            "sha256", password.encode("utf-8"), salt, int(iterations)
        )
        return hmac.compare_digest(candidate, expected)
    except (ValueError, TypeError):
        return False


def needs_rehash(stored: str) -> bool:
    """True when a stored credential is legacy plaintext or a weaker work factor."""
    if not stored or not stored.startswith("pbkdf2_sha256$"):
        return True
    try:
        iterations = int(stored.split("$")[1])
        return iterations < PBKDF2_ITERATIONS
    except (ValueError, IndexError):
        return True


# ─────────────────────────────────────────────────────────────────────
# JWT (HS256)
# ─────────────────────────────────────────────────────────────────────
def _b64url_encode(raw: bytes) -> str:
    return base64.urlsafe_b64encode(raw).rstrip(b"=").decode("ascii")


def _b64url_decode(segment: str) -> bytes:
    padding = "=" * (-len(segment) % 4)
    return base64.urlsafe_b64decode(segment + padding)


def _sign(signing_input: bytes) -> bytes:
    return hmac.new(_secret().encode("utf-8"), signing_input, hashlib.sha256).digest()


class TokenError(Exception):
    """Raised for a malformed, tampered, or expired token."""


def create_access_token(claims: dict, expires_minutes: int | None = None) -> str:
    minutes = DEFAULT_EXPIRY_MINUTES if expires_minutes is None else expires_minutes
    now = int(time.time())
    payload = {
        **claims,
        "iat": now,
        "nbf": now,
        "exp": now + minutes * 60,
        "iss": "dealflow360",
    }
    header = {"alg": JWT_ALGORITHM, "typ": "JWT"}

    segments = [
        _b64url_encode(json.dumps(header, separators=(",", ":"), sort_keys=True).encode()),
        _b64url_encode(json.dumps(payload, separators=(",", ":"), sort_keys=True).encode()),
    ]
    signing_input = ".".join(segments).encode("ascii")
    segments.append(_b64url_encode(_sign(signing_input)))
    return ".".join(segments)


def decode_access_token(token: str, leeway_seconds: int = 5) -> dict:
    """
    Verify signature and expiry, then return the claims.

    Raises TokenError on anything suspect. The signature is checked before the
    payload is trusted, and compared in constant time.
    """
    if not token or token.count(".") != 2:
        raise TokenError("Malformed token")

    header_b64, payload_b64, signature_b64 = token.split(".")
    signing_input = f"{header_b64}.{payload_b64}".encode("ascii")

    try:
        signature = _b64url_decode(signature_b64)
    except (ValueError, TypeError):
        raise TokenError("Malformed token signature")

    if not hmac.compare_digest(signature, _sign(signing_input)):
        raise TokenError("Invalid token signature")

    try:
        header = json.loads(_b64url_decode(header_b64))
        claims = json.loads(_b64url_decode(payload_b64))
    except (ValueError, TypeError):
        raise TokenError("Malformed token payload")

    # Reject alg confusion, including the "alg": "none" trick.
    if header.get("alg") != JWT_ALGORITHM:
        raise TokenError("Unsupported token algorithm")

    now = int(time.time())
    if "exp" in claims and now > int(claims["exp"]) + leeway_seconds:
        raise TokenError("Token has expired")
    if "nbf" in claims and now + leeway_seconds < int(claims["nbf"]):
        raise TokenError("Token is not yet valid")

    return claims
