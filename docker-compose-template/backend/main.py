from typing import List
from fastapi import Depends, FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from pydantic import BaseModel

from sqlalchemy.orm import Session
from base import SessionLocal, User


class UserView(BaseModel):
    login: str
    email: str

    class Config:
        orm_mode = True


class UserReturnView(BaseModel):
    login: str
    email: str
    id: int

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    login: str
    email: str
    password: str


templates = Jinja2Templates(directory="templates")

app = FastAPI()

@app.get('/', response_class=HTMLResponse)
def get(request: Request):
    return templates.TemplateResponse('index.html', {"request": request})

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get('/api/users', response_model=List[UserReturnView])
def get_users_api(db: Session = Depends(get_db)):
    return db.query(User).all()


@app.get('/users', response_class=HTMLResponse)
def get_users(
    request: Request, db: Session = Depends(get_db)):
    return templates.TemplateResponse(
        'users.html', {"request": request, "users": db.query(User).all()}
    )


@app.post('/users')
def register_user(
    user: UserCreate,
    db: Session = Depends(get_db),
):
    user = User(
        login=user.login,
        hashed_password=user.password + 'hash',
        email=user.email
    )
    db.add(user)
    db.commit()
    return 'ok'

