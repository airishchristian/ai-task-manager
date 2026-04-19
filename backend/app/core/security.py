from passlib.context import CryptContext

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
