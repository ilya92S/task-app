from pydantic import BaseModel

class UserLoginScheme(BaseModel):
    user_id: int
    access_token: str



class UserCreateScheme(BaseModel):
    username: str
    password: str
