from pydantic import BaseModel, EmailStr, ConfigDict

# TODO: UserCreate — what the client sends when registering
# Required fields: name (str), email (EmailStr), password (str)
# Think: what does the user fill out on a registration form?
class UserCreate(BaseModel):
    # your implementation
    name: str 
    email: EmailStr
    password: str


# TODO: UserResponse — what we send BACK after registration
# Fields: id (int), name (str), email (EmailStr)
# Notice: password is NOT here — we never send it back
# Add model_config to support ORM mode (same as TaskResponse)
class UserResponse(BaseModel):
    # your implementation
    id: int 
    name: str
    email: EmailStr
    model_config = ConfigDict(from_attributes=True)


class UserLogin(BaseModel):
    # TODO: What two fields does a login form need?
    # Your implementation goes here
    email: EmailStr
    password: str

class Token(BaseModel):
    # TODO: What does a successful login return?
    # Hint: Look at the OAuth2 standard — {"access_token": "...", "token_type": "bearer"}
    # Your implementation goes here
    access_token: str
    token_type: str = "bearer"