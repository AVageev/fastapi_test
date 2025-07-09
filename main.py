from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, EmailStr
from databases import Database
from models import users
from database import database
from passlib.hash import bcrypt

app = FastAPI()

origins = [
    "http://localhost:3000",  # React dev server
]

from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class UserRegister(BaseModel):
    email: EmailStr
    password: str
    password_confirm: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

@app.post("/register")
async def register(user: UserRegister):
    if user.password != user.password_confirm:
        raise HTTPException(status_code=400, detail="Пароли не совпадают")

    query = users.select().where(users.c.email == user.email)
    existing_user = await database.fetch_one(query)
    if existing_user:
        raise HTTPException(status_code=400, detail="Пользователь с таким email уже существует")

    hashed_password = bcrypt.hash(user.password)
    query = users.insert().values(email=user.email, password=hashed_password)
    await database.execute(query)
    return {"message": "Регистрация успешна"}

@app.post("/login")
async def login(user: UserLogin):
    query = users.select().where(users.c.email == user.email)
    db_user = await database.fetch_one(query)
    if not db_user:
        raise HTTPException(status_code=400, detail="Неверный логин или пароль")

    if not bcrypt.verify(user.password, db_user["password"]):
        raise HTTPException(status_code=400, detail="Неверный логин или пароль")

    # Тут должен быть реальный токен или сессия, но для простоты просто вернем сообщение
    return {"message": "Вход выполнен"}

@app.get("/dashboard")
async def dashboard():
    # Для примера просто возвращаем данные
    return {"message": "Добро пожаловать на дашборд!"}
