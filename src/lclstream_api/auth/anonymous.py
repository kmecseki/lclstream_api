from typing import Literal

from starlette.requests import HTTPConnection

from .base import AuthBackend, Principal


class Anonymous(AuthBackend):
    """Fixed user for development and tests."""

    type: Literal["anonymous"] = "anonymous"
    username: str = "none"

    async def authenticate(self, conn: HTTPConnection) -> Principal | None:
        return Principal(self.username)
