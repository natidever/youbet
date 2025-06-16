
from datetime import datetime, timedelta, timezone
from sqlmodel import Session, select

from app.models.core_models import User

from passlib.context import CryptContext

from jose import jwt ,JWTError

from app.config.settings import Settings
from app.config.logger import logger 




settings=Settings()


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def authenticate_user(session:Session, username: str, password: str):
    try:
        statement=select(User).where(User.username==username)
        result=session.exec(statement)
    


        user=result.one_or_none() 
        print(f"user_result:{user}")
        if not user:
            return "Invalid Credentials"
        if not verify_password(password, user.password_hash):
            return False
        return user
    except Exception as error:
        print(f"Error:{error}")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)




def create_token(data:dict,expire_date:timedelta| None=None):
    try:
        to_encode=data.copy()
        if expire_date:
            expire=datetime.now(timezone.utc)+expire_date
        else:
            expire=datetime.now(timezone.utc)+timedelta(days=1)

        to_encode.update({"expire":expire.isoformat()})


        jwt_encoded=jwt.encode(to_encode,settings.SECRETE_KEY,algorithm=settings.ALGORITHM)
        # jwt_encoded=jwt.encode(to_encode,SECRETE_KEY,algorithm=ALGORITHM)
        logger.debug(f"ALGO:{settings.ALGORITHM} SECRETE:{settings.SECRETE_KEY}")

        print(f"{jwt_encoded}")

        
        return jwt_encoded
    except JWTError as error:
        logger.error(f"jwt_error:{error}")
        raise Exception("JWT_EXCEPTION_CREATE_TOKEN")

   










