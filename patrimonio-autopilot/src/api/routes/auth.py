from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.api.auth import create_access_token, hash_password, verify_password
from src.api.schemas import AuthTokenRead, UserLoginRequest, UserRegisterRequest
from src.data.database import get_db
from src.data.models import User


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=AuthTokenRead, status_code=status.HTTP_201_CREATED)
def register(payload: UserRegisterRequest, db: Session = Depends(get_db)) -> AuthTokenRead:
    email = payload.email.strip().lower()
    existing = db.query(User).filter(User.email == email).first()
    if existing is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already exists")
    user = User(email=email, password_hash=hash_password(payload.password))
    db.add(user)
    db.commit()
    db.refresh(user)
    token = create_access_token(user_id=user.id, email=user.email)
    return AuthTokenRead(access_token=token)


@router.post("/login", response_model=AuthTokenRead)
def login(payload: UserLoginRequest, db: Session = Depends(get_db)) -> AuthTokenRead:
    email = payload.email.strip().lower()
    user = db.query(User).filter(User.email == email).first()
    if user is None or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    token = create_access_token(user_id=user.id, email=user.email)
    return AuthTokenRead(access_token=token)

