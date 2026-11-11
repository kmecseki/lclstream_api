from typing import Literal

import jwt
from starlette.requests import HTTPConnection

from .base import AuthBackend, Principal

# Authorization header scheme for bearer tokens (RFC 6750).
BEARER_PREFIX = "Bearer "


class ForwardedJWT(AuthBackend):
    """Read identity from a Bearer JWT an auth proxy has already validated.

    oauth2-proxy with --skip-jwt-bearer-tokens forwards the token but sets
    no identity headers. The signature is NOT checked here, so this is only
    safe behind that proxy.
    """

    type: Literal["forwarded_jwt"] = "forwarded_jwt"
    # First non-empty claim names the user.
    claims: list[str] = ["email", "preferred_username"]

    async def authenticate(self, conn: HTTPConnection) -> Principal | None:
        payload = _jwt_payload(conn.headers.get("Authorization"))
        user = next((payload[c] for c in self.claims if payload.get(c)), None)
        if not user:
            return None
        return Principal(user)


def _jwt_payload(authorization: str | None) -> dict:
    """Decode a Bearer JWT's claims without verifying it; {} if malformed."""
    if not authorization or not authorization.startswith(BEARER_PREFIX):
        return {}
    token = authorization.removeprefix(BEARER_PREFIX)
    try:
        return jwt.decode(token, options={"verify_signature": False})
    except jwt.InvalidTokenError:
        return {}
