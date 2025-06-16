

from fastapi import Depends,HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt ,JWTError



from app.constants.role import UserRole
from app.config.settings import Settings
from app.config.logger import logger
# SECRETE_KEY="SDF"
# ALGORITHM="HS256"

settings=Settings()

oAuth2_schme=OAuth2PasswordBearer(tokenUrl="auth/token")

def get_current_user(token:str=Depends(oAuth2_schme)):
    try:
        decoded=jwt.decode(token,settings.SECRETE_KEY,algorithms=[settings.ALGORITHM])
       
        print(f"decodedx:{ decoded.get("role")}")
        # user_id=decoded.values(user_id)
        role=decoded.get("role")
        logger.debug(f"current_user_access:{role}")

        if  not role :
            raise HTTPException(status_code=401, detail="Invalid token")
        return {"role":role}
    except JWTError:
        raise HTTPException(status_code=401, detail="Token error")
    
def require_role(required_roles:list[UserRole]):
    def role_checker(user=Depends(get_current_user)):
        print(f"xuser:{user}")
        # check if he above role is inside the given user 
        if user["role"] not in required_roles:
            raise HTTPException(status_code=401,detail="Access  denied")
        return user 
    return role_checker






