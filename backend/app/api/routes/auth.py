from fastapi import APIRouter, HTTPException
from sqlmodel import Session, select
from ...database import engine
from ...models.user import User
from ...schemas.user import UserCreate, UserResponse, UserLogin, Token
from ...core.security import hash_password, verify_password, create_access_token


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

@router.post("/login", response_model=Token)
def login(user_credentials: UserLogin):
    """
    POST /auth/login
    Verifies credentials and returns a JWT token.

    TODO:
    - Open a Session
    - Query the database for a user with the matching email
      Hint: select(User).where(User.email == user_credentials.email)
    - If no user found → raise HTTPException 401
      Why 401 and not 404? Think about this — what are we protecting?
    - Use verify_password() to check the submitted password against the stored hash
    - If password is wrong → raise HTTPException 401
      Use the SAME error message as "user not found" — why is this important?
    - Call create_access_token(data={"sub": user.email})
    - Return {"access_token": token, "token_type": "bearer"}
    """
    # Your implementation goes here
    with Session(engine) as session:
        statement = select(User).where(User.email == user_credentials.email)
        result = session.exec(statement).first()
        if result is None:
            raise HTTPException(status_code=401, detail="Invalid Email or Password")
        is_verified = verify_password(user_credentials.password, result.hashed_password)
        if not is_verified:
            raise HTTPException(status_code=401, detail="Invalid Email or Password")
        token = create_access_token(data={"sub": user_credentials.email})
        return {"access_token": token, "token_type": "bearer"}


