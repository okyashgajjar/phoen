"""
Shared login helper for the test suite.

The old helper returned {"Authorization": f"Bearer {user_id}"}, because the
bearer token used to be the user's own id. That is exactly the hole the auth
rewrite closed, so tests now perform a real login and use the signed JWT.

Persona ids map to seeded email addresses so existing tests keep reading the
way they did — auth("rep_marcus") still works, it just authenticates properly.
"""

from functools import lru_cache

EMAILS = {
    "rep_marcus": "marcus@dealflow360.com",
    "kavita_sharma": "kavita@dealflow360.com",
    "rep_rachel": "rachel@dealflow360.com",
    "rep_sarah": "sarah@dealflow360.com",
    "mgr_sarah": "sarah@dealflow360.com",
    "vikram_singhania": "vikram@dealflow360.com",
    "fin_david": "david@dealflow360.com",
    "alex_admin": "alex@dealflow360.com",
    "admin_1": "admin@dealflow360.com",
    # portal / customer personas
    "cust_acme": "acme@portal.dealflow360.com",
    "cust_zenith": "zenith@portal.dealflow360.com",
    "customer": "acme@portal.dealflow360.com",
    # role aliases
    "sales_rep": "kavita@dealflow360.com",
    "manager": "vikram@dealflow360.com",
    "finance": "david@dealflow360.com",
    "admin": "alex@dealflow360.com",
}

DEFAULT_PASSWORD = "password"


@lru_cache(maxsize=None)
def token_for(client_id: int, who: str) -> str:
    from main import app
    from fastapi.testclient import TestClient

    email = EMAILS.get(who, who)
    resp = TestClient(app).post(
        "/api/v1/auth/login", json={"email": email, "password": DEFAULT_PASSWORD}
    )
    assert resp.status_code == 200, f"login failed for {who} ({email}): {resp.text}"
    return resp.json()["access_token"]


def auth(who: str) -> dict:
    """Authorization header for a persona id, role name, or email."""
    return {"Authorization": f"Bearer {token_for(0, who)}"}
