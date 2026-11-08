from typing import Annotated

from pydantic import Field

from .anonymous import Anonymous
from .base import AuthBackend, Principal
from .chain import AuthChain
from .forwarded_jwt import ForwardedJWT
from .mtls import MTLS
from .trusted_headers import TrustedHeaders

__all__ = [
    "MTLS",
    "Anonymous",
    "AuthConfig",
    "AuthBackend",
    "AuthChain",
    "ForwardedJWT",
    "Principal",
    "TrustedHeaders",
]

AuthConfig = Annotated[
    Anonymous | TrustedHeaders | ForwardedJWT | MTLS | AuthChain,
    Field(discriminator="type"),
]

# needs to be rebuilt because of the reference to AuthConfig in AuthChain
AuthChain.model_rebuild()
