from Todos.Router.todos import templates

from ..database import SessionLocal, engine
from fastapi import FastAPI, Depends, HTTPException, Path, APIRouter, Form, Request
from ..models import Users
from ..database import engine
from typing import Annotated
from passlib.context import CryptContext
from pydantic import BaseModel, Field
from sqlalchemy.dialects.postgresql import array
from sqlalchemy.orm import Session
from starlette import status
from .auth import get_current_user
from starlette.responses import RedirectResponse
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates


router = APIRouter(
    prefix="/user",
    tags=["users"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserVerification(BaseModel):
    password: str
    new_password: str = Field(min_length=6)

### Pages ###
@router.get("/edit-password", response_class=HTMLResponse)
async def render_edit_user_password(request: Request):
    try:
        user = await get_current_user(request.cookies.get('access_token'))
        if user is None:
            return redirect_to_login()

        return templates.TemplateResponse("edit-user-password.html", {"request": request, "user": user})
    except:
        return redirect_to_login()

@router.post("/edit-password", response_class=HTMLResponse)
async def user_password_change(request: Request, db: db_dependency, username: str = Form(...), password: str = Form(...),
                               password2: str = Form(...)):
    try:
        user = await get_current_user(request.cookies.get('access_token'))
        if user is None:
            return redirect_to_login()

        user_data = db.query(Users).filter(Users.username == username).first()

        msg = "Invalid username or password"
        if user_data is not None:
            if username == user_data.username and password == password2:
                user_data.hashed_password = bcrypt_context.hash(password2)
                db.add(user_data)
                db.commit()
                msg = "Password updated successfully"

        return templates.TemplateResponse("edit-user-password.html", {"request": request, "user": user, "msg": msg})
    except:
        return redirect_to_login()


### Endpoints ###
@router.get("/", status_code=status.HTTP_200_OK)
async def read_users(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")
    return db.query(Users).filter(Users.id == user.get('id')).first()
    # if user_model is None:
    #     raise HTTPException(status_code=404, detail="User not found")
    # return user_model

@router.put("/change_password", status_code=status.HTTP_204_NO_CONTENT)
async def change_password(user: user_dependency, db: db_dependency
                          , user_verification: UserVerification):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")
    user_model = db.query(Users).filter(Users.id == user.get('id')).first()

    if not bcrypt_context.verify(user_verification.password, user_model.hashed_password):
        raise HTTPException(status_code=401, detail="error on password change.")
    user_model.hashed_password = bcrypt_context.hash(user_verification.new_password)
    db.add(user_model)
    db.commit()

@router.put("/phone_number/{phone_number}", status_code=status.HTTP_204_NO_CONTENT)
async def change_phone_number(user: user_dependency, db: db_dependency, phone_number: str):

    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")

    user_model = db.query(Users).filter(Users.id == user.get('id')).first()
    user_model.phone_number = phone_number
    db.add(user_model)
    db.commit()