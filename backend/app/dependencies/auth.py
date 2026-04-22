from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, HTTPBearer, HTTPAuthorizationCredentials
from sqlmodel import Session, select
from app.models.user import User
from app.core.security import verify_token
from app.dependencies.database import get_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
bearer_scheme = HTTPBearer()

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_db)
):
    token = credentials.credentials  # extracts the token string
    # TODO: Call verify_token(token) — what does it return?
    # TODO: If the result is None, raise HTTPException 401
    #       Use: status.HTTP_401_UNAUTHORIZED
    #       Detail: "Could not validate credentials"
    #       Headers: {"WWW-Authenticate": "Bearer"}
    # TODO: Use the email from the token to query the User table
    # TODO: If user not found, raise 401
    # TODO: Return the user
    verified = verify_token(token)
    if verified is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                            detail="Could not validate credentials",
                            headers={"WWW-Authenticate": "Bearer"}
        )
    
    statement = select(User).where(User.email == verified)
    result = db.exec(statement).first()

    if result is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"}
        )
    return result
    
def get_current_active_user(
    current_user = Depends(get_current_user)
):
    # TODO: For now, just return current_user
    # (In Lesson 14 you'll add an is_active check)
    return current_user