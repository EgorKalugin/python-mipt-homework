from datetime import datetime, timedelta, timezone
from typing import Annotated, Any

import jwt
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError
from pwdlib import PasswordHash
from pydantic import BaseModel, ConfigDict
from sqlalchemy import select
from sqlalchemy.orm import Session

from dz9.auth import User
from dz9.main import engine

# openssl rand -hex 32
SECRET_KEY = "1548855d3ceac49de6c17c795933218bcf2b240eb4c8eb07f3702a043480e8bb"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
SALT = "283f1f0dc040d12793a76657cb8084cea722a67302687fda804d8a5f80b3c69d"


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class UserSchema(BaseModel):
    username: str

    model_config = ConfigDict(from_attributes=True)


class UserInDBSchema(UserSchema):
    password: str


password_hash = PasswordHash.recommended()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

auth_router = APIRouter(prefix="/auth", tags=["Auth"])


def verify_password(plain_password: str, hashed_password: str):
    print(plain_password)
    print(hashed_password)
    return password_hash.verify(SALT + plain_password, hashed_password)


def get_password_hash(password: str):
    return password_hash.hash(SALT + password)


def get_session():
    with Session(engine) as session:
        yield session


def register_user(
    db: Session,
    username: str,
    password: str,
):
    db.add(User(username=username, password=get_password_hash(password)))
    db.commit()


def get_user(
    db: Session,
    username: str,
) -> UserInDBSchema | None:
    res = db.scalar(select(User).where(User.username == username))
    if res:
        return UserInDBSchema.model_validate(res)
    return None


def add_user(username: str, password: str):
    User(username=username, password=password_hash.hash(SALT + password))


def get_current_user(
    db: Annotated[Session, Depends(get_session)],
    token: Annotated[str, Depends(oauth2_scheme)],
) -> UserSchema:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        token_data = TokenData(username=username)
        if token_data.username is None:
            raise credentials_exception
    except InvalidTokenError:
        raise credentials_exception
    user = get_user(db, token_data.username)
    if user is None:
        raise credentials_exception
    return user


def authenticate_user(
    db: Annotated[Session, Depends(get_session)],
    username: str,
    password: str,
):
    user = get_user(db, username)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user


def create_access_token(data: dict[str, Any], expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


@auth_router.post("/token")
def login_for_access_token(
    db: Annotated[Session, Depends(get_session)],
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


@auth_router.get("/users/me")
def read_users_me(
    current_user: Annotated[UserSchema, Depends(get_current_user)],
):
    return current_user


@auth_router.post("/register")
def register(
    new_user: UserInDBSchema,
    db: Annotated[Session, Depends(get_session)],
):
    register_user(db, new_user.username, new_user.password)
