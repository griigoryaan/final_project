from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, models, schemas
from app.database import Base, engine, SessionLocal

# Создание приложения FastAPI
app = FastAPI()

# Инициализация базы данных
Base.metadata.create_all(bind=engine)

# Dependency для получения сессии базы данных
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"message": "Welcome to Telecom API!"}

# Маршруты для Operator
@app.post("/operators/", response_model=schemas.Operator)
def create_operator(operator: schemas.OperatorCreate, db: Session = Depends(get_db)):
    return crud.create_operator(db=db, operator=operator)

@app.get("/operators/{operator_id}", response_model=schemas.Operator)
def read_operator(operator_id: int, db: Session = Depends(get_db)):
    db_operator = crud.get_operator(db, operator_id)
    if db_operator is None:
        raise HTTPException(status_code=404, detail="Operator not found")
    return db_operator

@app.get("/operators/", response_model=list[schemas.Operator])
def read_operators(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_operators(db, skip=skip, limit=limit)
