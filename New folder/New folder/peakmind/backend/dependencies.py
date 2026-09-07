"""
JWT validation dependency for FastAPI endpoints.

Validates Clerk-issued JWTs by fetching the JWKS from Clerk's well-known endpoint
and verifying the token signature. Extracts the `sub` (Clerk user ID) claim.

Usage:
    @router.get("/")
    def my_endpoint(user_id: str = Depends(get_current_user_id), ...):
        ...
"""
import os
import httpx
import jwt as pyjwt
from functools import lru_cache
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

_security = HTTPBearer(auto_error=True)

CLERK_FRONTEND_API = os.getenv("CLERK_FRONTEND_API", "")


@lru_cache(maxsize=1)
def _get_jwks() -> dict:
    """Fetch Clerk's JWKS (cached for the process lifetime)."""
    jwks_url = f"https://{CLERK_FRONTEND_API}/.well-known/jwks.json"
    try:
        response = httpx.get(jwks_url, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Could not fetch JWKS from Clerk: {exc}",
        )


def _decode_token(token: str) -> dict:
    """Validate and decode a Clerk JWT, returning the claims."""
    jwks = _get_jwks()

    try:
        header = pyjwt.get_unverified_header(token)
    except pyjwt.exceptions.DecodeError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid token header: {exc}",
        )

    # Find the matching key
    kid = header.get("kid")
    matching_key = next(
        (k for k in jwks.get("keys", []) if k.get("kid") == kid), None
    )
    if matching_key is None:
        # Refresh JWKS cache and retry once (key rotation)
        _get_jwks.cache_clear()
        jwks = _get_jwks()
        matching_key = next(
            (k for k in jwks.get("keys", []) if k.get("kid") == kid), None
        )

    if matching_key is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token signing key not found in JWKS",
        )

    try:
        public_key = pyjwt.algorithms.RSAAlgorithm.from_jwk(matching_key)
        payload = pyjwt.decode(
            token,
            public_key,
            algorithms=["RS256"],
            options={"verify_aud": False},
        )
        return payload
    except pyjwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired"
        )
    except pyjwt.InvalidTokenError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Invalid token: {exc}"
        )


def get_current_user_id(
    credentials: HTTPAuthorizationCredentials = Depends(_security),
) -> str:
    """FastAPI dependency that returns the authenticated Clerk user ID (sub claim)."""
    payload = _decode_token(credentials.credentials)
    user_id: str | None = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token missing 'sub' claim",
        )
    return user_id
