

from fastapi import Depends,HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt ,JWTError


from app.constants.role import UserRole
from app.config.settings import Settings
# SECRETE_KEY="SDF"
# ALGORITHM="HS256"

settings=Settings()

oAuth2_schme=OAuth2PasswordBearer(tokenUrl="auth/token")

def get_current_user(token:str=Depends(oAuth2_schme)):
    try:
        decoded=jwt.decode(token,settings.SECRETE_KEY,algorithms=[settings.ALGORITHM])
        user_id=decoded.values(user_id)
        role=decoded.values("roles")

        if not user_id or not role :
            raise HTTPException(status_code=401, detail="Invalid token")
        return {user_id:user_id,role:role}
    except JWTError:
        raise HTTPException(status_code=401, detail="Token error")
    
def require_role(required_role:list[UserRole]):
    def role_checker(user=Depends(get_current_user)):
        # check if he above role is inside the given user 
        if user["role"] not in require_role:
            raise HTTPException(status_code=401,detail="Access  denied")
        return user 
    return role_checker






