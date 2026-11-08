from typing import Literal

from starlette.requests import HTTPConnection

from .base import AuthBackend, Principal


class TrustedHeaders(AuthBackend):
    """Read identity from headers an auth proxy sets, e.g. oauth2-proxy.

    Only safe if every request reaches the app through that proxy, since
    any client can send these headers.
    """

    type: Literal["trusted_headers"] = "trusted_headers"
    user_header: str = "X-Auth-Request-User"

    async def authenticate(self, conn: HTTPConnection) -> Principal | None:
        user = conn.headers.get(self.user_header)
        if not user:
            return None
        return Principal(user)
