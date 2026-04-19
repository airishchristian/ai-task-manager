from fastapi import APIRouter, HTTPException
from sqlmodel import Session, select
from ...database import engine
from ...models.user import User
from ...schemas.user import UserCreate,UserResponse
from ...core.security import hash_password


router = APIRouter()

@router.post("/register", response_model=UserResponse, status_code=201)
def register(user_data: UserCreate):
    """
    POST /auth/register
    Creates a new user account with a hashed password.

    TODO:
    1. Open a Session
    2. Check if a user with this email already exists
       - Use select(User).where(User.email == user_data.email)
       - If found: raise HTTPException 400 with message "Email already registered"
       WHY: We must enforce uniqueness — two accounts with the same email breaks login
    3. Hash the password using hash_password()
    4. Create a User object
       - Do NOT pass user_data.password directly
       - Pass hashed_password=hash_password(user_data.password) instead
    5. Add, commit, refresh, return
    """
    # your implementation
    with Session(engine) as session:
        statement = select(User).where(User.email == user_data.email)
        result = session.exec(statement).first()
        if result is not None:
            raise HTTPException(status_code=400, detail="Email already registered.")
        user_data = user_data.model_dump()
        user_data["hashed_password"] = hash_password(user_data["password"])
        user_data.pop("password")
        user = User(**user_data)
        session.add(user)
        session.commit()
        session.refresh(user)
        return user

