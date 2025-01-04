from fastapi import FastAPI
from app.database import Base, engine

# Создание приложения FastAPI
app = FastAPI()

# Инициализация базы данных
Base.metadata.create_all(bind=engine)

@app.get("/")
def read_root():
    return {"message": "Welcome to Telecom API!"}
