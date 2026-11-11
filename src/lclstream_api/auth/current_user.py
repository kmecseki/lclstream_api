"""FastAPI dependency naming the user behind each request."""

from typing import Annotated

from fastapi import Depends, HTTPException, Request, status
from svcs.fastapi import DepContainer

from .base import AuthBackend


async def current_user(request: Request, services: DepContainer) -> str:
    backend = await services.aget(AuthBackend)
    principal = await backend.authenticate(request)
    if principal is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Not authenticated.")
    return principal.identity


CurrentUser = Annotated[str, Depends(current_user)]
