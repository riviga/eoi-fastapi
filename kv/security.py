from datetime import datetime, timedelta, timezone
from fastapi import Depends, HTTPException, status
from fastapi.security import APIKeyHeader, HTTPBasic, HTTPBasicCredentials, OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError
import jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from logger import log

username = "Rick"
password = "supersecretkey"

credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# API key header
apikey_security = APIKeyHeader(name="x-apikey")

def validate_apikey(value: str):
    if(value != password):
        raise credentials_exception


# HTTP Basic
basic_security = HTTPBasic()
    
def validate_basic(credentials: HTTPBasicCredentials):
    if credentials.username != username or credentials.password != password:
        raise credentials_exception
    
    
# Auth2    
SECRET_KEY = "05f0955be8ddd0643fa86669a40deff4834601301e53c62bf85ee4097624c184"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


fake_users_db = {
    "rsanchez": {
        "username": "rsanchez",
        "full_name": "Rick Sanchez",
        "email": "rsanchez@picke.com",
        "hashed_password": "$2b$12$hn4P/9juI0efvfiY421g8.9GEAlIu5LjFVFfGd/ZX2pjMlvOcS7FC",
        "disabled": False,
    },
    "msmith": {
        "username": "msmith",
        "full_name": "Morty Smith",
        "email": "msmith@geez.com",
        "hashed_password": "$2b$12$H9BH6f4H31aHAZSiET09pexEwk4pMjgdcWr4zlG3kNMTkWDKyjKxa",
        "disabled": True,
    }
}

class UserSchema(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None
    hashed_password: str
    

def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(username: str):
    if username not in fake_users_db:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username")
    return UserSchema(**fake_users_db[username])
    
    
def authenticate_user(form_data: OAuth2PasswordRequestForm):
    log.info("authenticate_user form_data [{form_data}]")
    user = get_user(form_data.username)
    log.info(f"user [{user}]")
    if not pwd_context.verify(form_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect password")    


def encode_token(payload: str):
    try:
        return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    except InvalidTokenError as ex:
        log.error(f"InvalidTokenError: {ex}")
        raise credentials_exception    


def decode_token(token: str):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])         
    except InvalidTokenError as ex:
        log.error(f"InvalidTokenError: {ex}")
        raise credentials_exception
    
    
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    payload = data.copy()
    expires_delta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    expire = datetime.now(timezone.utc) + expires_delta    
    payload.update({"exp": expire})
    encoded_jwt = encode_token(payload)     
    return encoded_jwt


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/kv/token")
async def get_validated_active_user(token: str = Depends(oauth2_scheme)):     
    log.info(f"token [{token}]")
    payload = decode_token(token)
    log.info(f"payload [{payload}]")
    username: str = payload.get("sub")
    log.info(f"username [{username}]")
    if username is None:
        raise credentials_exception   
    user = get_user(username)    
    log.info(f"user.disabled [{user.disabled}]")
    if user.disabled:        
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Disabled user")
    return user
