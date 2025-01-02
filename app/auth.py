from jose import JWTError, jwt
from datetime import datetime,timedelta
from fastapi import APIRouter,HTTPException,status
from models import User

SECRET_KEY="your_serect_key"
ALGORITHM ="HS256"
ACCESS_TOKEN_EXPIRE_MINUTE=30

#Create JWT token
def create_access_token(
        data:dict,
        expires_delta:timedelta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTE)):
    to_encode=data.copy()
    expire=datetime.utcnow + expires_delta
    to_encode.update({"exp":expire})
    encode_jwt = jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return encode_jwt
#Verify the JWT token
def verify_token(token:str):
    try:
        payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None

router=APIRouter()

#Login router to issue JWT
@router.post("\token")
async def login_for_accsess_token(user:User):
    # todo: check user if exist and validate password
    access_token=create_access_token(data={"sub":user.username})
    return {"access_token":access_token,"token_type":"hearer"}

def get_current_user(token:str):
    user=verify_token(token)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid_token")
    return user