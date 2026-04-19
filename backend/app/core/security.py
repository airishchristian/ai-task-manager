from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
import jwt
import os

# TODO: Create a CryptContext instance
# - schemes should be ["bcrypt"]
# - deprecated should be "auto"
# WHY: This tells passlib to use bcrypt as the hashing algorithm
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """
    TODO: Use pwd_context to hash the plain password
    Hint: Look up CryptContext.hash()
    """
    # your implementation
    hashed = pwd_context.hash(password)
    return hashed
    


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    TODO: Use pwd_context to verify plain_password against hashed_password
    Hint: Look up CryptContext.verify()
    Returns True if they match, False otherwise
    """
    # your implementation
    is_verified = pwd_context.verify(plain_password, hashed_password)
    return is_verified

SECRET_KEY = os.environ.get("SECRET_KEY")
ALGORITHM = os.environ.get("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

def create_access_token(data: dict) -> str:
    """
    Creates a signed JWT token.

    TODO:
    - Make a copy of `data` so you don't mutate the original
    - Calculate the expiry time:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    - Add "exp" key to your copy with the expire value
    - Use jwt.encode(your_copy, SECRET_KEY, algorithm=ALGORITHM) to create the token
    - Return the token
    
    Hint: Read PyJWT docs → https://pyjwt.readthedocs.io/en/stable/usage.html
    """
    # Your implementation goes here
    data_copy = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    data_copy["exp"] = expire
    token = jwt.encode(data_copy, SECRET_KEY, algorithm=ALGORITHM)
    return token

def verify_token(token: str) -> str | None:
    """
    Verifies a JWT token and returns the subject (email).

    TODO:
    - Use jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM]) inside a try/except
    - Extract the "sub" field from the decoded payload
    - If "sub" is None, return None
    - Return the email string
    - Catch jwt.PyJWTError — return None if anything goes wrong
    
    Hint: What exception does PyJWT raise for invalid/expired tokens?
    """
    # Your implementation goes here
    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return decoded.get("sub") # Returns None if "sub" is not in there
    except jwt.PyJWTError:
        return None
