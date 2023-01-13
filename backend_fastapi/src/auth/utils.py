from fastapi import HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from passlib.context import CryptContext
from ..settings import settings

ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def encode_token(payload: dict):
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=ALGORITHM)


def decode_token(authorization: str):
    return jwt.decode(authorization, settings.SECRET_KEY, algorithms=ALGORITHM)


def get_payload(authorization: str):
    try:
        token = authorization.replace("Bearer ", "")
        # Decode the token using the secret key
        payload = decode_token(token)
        return payload
    # except jwt.ExpiredSignatureError:
    #     raise ValueError("Token has expired.")
    except:  # noqa
        # raise ValueError("Invalid token.")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token. Access denied. Try Logging in with an authorized account",
        )


def checkAdmin(request: Request):
    payload = get_payload(request.headers.get("Authorization"))
    if not payload or payload.get("role") == "customer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Access denied."
        )


def checkCustomer(request: Request, id: int):
    payload = get_payload(request.headers.get("Authorization"))
    if not payload or (payload.get("role") == "customer" and payload.get("id") != id):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Access denied."
        )
