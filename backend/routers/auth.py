from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from motor.motor_asyncio import AsyncIOMotorDatabase
from datetime import timedelta

from database import db
from models.user import User, UserCreate, UserPublic, Token
from security import get_password_hash, verify_password, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)

# Dependency to get the database instance
def get_database() -> AsyncIOMotorDatabase:
    return db.db

@router.post("/register", response_model=UserPublic, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_in: UserCreate,
    database: AsyncIOMotorDatabase = Depends(get_database)
):
    """Create a new user in the database."""
    existing_user = await database.users.find_one({"email": user_in.email})
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A user with this email already exists.",
        )

    hashed_password = get_password_hash(user_in.password)
    
    user_to_create = User(
        username=user_in.username,
        email=user_in.email,
        hashed_password=hashed_password,
        role=user_in.role
    )

    new_user = await database.users.insert_one(
        user_to_create.model_dump(by_alias=False, exclude={"id"})
    )
    
    created_user = await database.users.find_one({"_id": new_user.inserted_id})
    return created_user

@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    database: AsyncIOMotorDatabase = Depends(get_database)
):
    """Authenticate user and return a JWT access token."""
    user = await database.users.find_one({"email": form_data.username}) # form username is email
    if not user or not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["email"]}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}