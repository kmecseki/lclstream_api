from typing import TYPE_CHECKING, Literal

from starlette.requests import HTTPConnection

from .base import AuthBackend, Principal

if TYPE_CHECKING:
    from . import AuthConfig


class AuthChain(AuthBackend):
    """Try backends in order; the first that finds a user wins."""

    type: Literal["chain"] = "chain"
    backends: list["AuthConfig"]  # TODO: quotes used for circular import

    async def authenticate(self, conn: HTTPConnection) -> Principal | None:
        for backend in self.backends:
            result = await backend.authenticate(conn)
            if result is not None:
                return result
        return None
