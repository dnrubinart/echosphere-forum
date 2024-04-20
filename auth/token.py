from datetime import datetime, timedelta
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from fastapi import Depends, HTTPException, status


SECRET_KEY = "4f1feeca525de4cdb064656007da3edac7895a87ff0ea865693300fb8b6e8f9c"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRATION_MINS = 30

oauth2_bearer = OAuth2PasswordBearer(tokenUrl="/auth/token")


def create_access_token(username: str, user_id: int, expires_in: timedelta):
    encode = {"sub": username, "id": user_id}
    expiration = datetime.now() + expires_in
    encode.update({"exp": expiration})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        user_id: int = payload.get("id")
        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="Could not validate user.")
        return {"username": username, "id": user_id}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Could not validate user.")