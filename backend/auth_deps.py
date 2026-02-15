"""Auth dependencies: resolve user_id from JWT (NextAuth) or fall back to session."""

from typing import Annotated

import jwt
from fastapi import Depends, Header
from sqlalchemy.orm import Session

from config import NEXTAUTH_SECRET
from db import get_db
from db.models import User


def get_optional_user_id(
    authorization: Annotated[str | None, Header()] = None,
    db: Annotated[Session, Depends(get_db)] = None,
) -> str | None:
    """Resolve user_id from Authorization Bearer JWT (NextAuth). Ensures user exists in DB.

    If no token or invalid, returns None (caller should use X-Session-Id for anonymous).
    """
    if not authorization or not authorization.startswith("Bearer "):
        return None
    token = authorization[7:].strip()
    if not token or not NEXTAUTH_SECRET:
        return None
    try:
        payload = jwt.decode(
            token,
            NEXTAUTH_SECRET,
            algorithms=["HS256"],
            options={"verify_exp": True},
        )
    except jwt.InvalidTokenError:
        return None
    user_id = payload.get("sub")
    if not user_id:
        return None
    # Ensure user row exists (upsert from JWT claims)
    user = db.get(User, user_id)
    if not user:
        user = User(
            id=user_id,
            email=payload.get("email"),
            name=payload.get("name"),
            avatar_url=payload.get("picture"),
        )
        db.add(user)
        db.commit()
        db.refresh(user)
    elif payload.get("name") or payload.get("email") or payload.get("picture"):
        user.name = payload.get("name") or user.name
        user.email = payload.get("email") or user.email
        user.avatar_url = payload.get("picture") or user.avatar_url
        db.commit()
    return user_id


def get_identity(
    user_id: Annotated[str | None, Depends(get_optional_user_id)] = None,
    x_session_id: Annotated[str | None, Header(alias="X-Session-Id")] = None,
) -> tuple[str | None, str | None]:
    """Return (user_id, session_id) for keying progress/design. One of them may be set."""
    return (user_id, x_session_id)
