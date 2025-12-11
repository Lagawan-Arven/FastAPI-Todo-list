from passlib.context import CryptContext

from jose import jwt

secret_key = "my_secret"
algorithm = "HS256"

pwd_context = CryptContext(schemes=["bcrypt"],deprecated="auto")

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(password: str,hashed_password: str): 
    return pwd_context.verify(password,hashed_password)

def create_access_token(data: dict):
    to_encode = data.copy()
    return jwt.encode(to_encode,secret_key,algorithm=algorithm)