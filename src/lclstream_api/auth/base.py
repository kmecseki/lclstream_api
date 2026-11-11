from dataclasses import dataclass

from pydantic import BaseModel, ConfigDict
from starlette.requests import HTTPConnection


@dataclass(frozen=True)
class Principal:
    identity: str


class AuthBackend(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    # Each backend narrows it, e.g. Literal["mtls"].
    type: str

    async def authenticate(self, conn: HTTPConnection) -> Principal | None:
        """Who sent the request, or None if this backend can't tell."""
        raise NotImplementedError
