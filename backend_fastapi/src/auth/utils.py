from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from passlib.context import CryptContext

SECRET_KEY = "99d243a20fc52c7b11b01e64239eb37e90ce7b482f4901683f2a7663ab314416"
ALGORITHM = "HS256"


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def encode_token(payload: dict):
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def decode_token(authorization: str):
    return jwt.decode(authorization, SECRET_KEY, algorithms=ALGORITHM)
