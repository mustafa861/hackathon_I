"""
API endpoints for user authentication (signup, signin).
"""

from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from ..core.database import get_db
from ..models.user import UserCreate, UserResponse, UserDB
from ..core.auth import get_password_hash, authenticate_user, create_access_token

router = APIRouter(prefix="/auth", tags=["auth"])

# Request models
class UserSignupRequest(UserCreate):
    pass  # Inherit from UserCreate which already has all necessary fields

class UserSigninRequest(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str

@router.post("/signup", response_model=UserResponse)
async def signup(request: UserSignupRequest, db: AsyncSession = Depends(get_db)):
    """
    Create a new user account.
    """
    # Check if user already exists
    existing_user_result = await db.execute(
        select(UserDB).filter((UserDB.username == request.username) | (UserDB.email == request.email))
    )
    existing_user = existing_user_result.scalar_one_or_none()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or email already registered"
        )

    # Create new user
    hashed_password = get_password_hash(request.password)
    db_user = UserDB(
        username=request.username,
        email=request.email,
        hashed_password=hashed_password,
        software_hardware_background=request.software_hardware_background
    )

    db.add(db_user)

    try:
        await db.commit()
        await db.refresh(db_user)

        # Return response using the UserResponse model
        return UserResponse(
            id=db_user.id,
            username=db_user.username,
            email=db_user.email,
            software_hardware_background=db_user.software_hardware_background,
            created_at=db_user.created_at,
            updated_at=db_user.updated_at
        )
    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or email already registered"
        )

@router.post("/signin", response_model=TokenResponse)
async def signin(request: UserSigninRequest, db: AsyncSession = Depends(get_db)):
    """
    Authenticate a user and return an access token.
    """
    user = await authenticate_user(db, request.username, request.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create access token
    access_token = create_access_token(data={"sub": user.username})

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }