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

# Маршруты для Subscriber
@app.post("/subscribers/", response_model=schemas.Subscriber)
def create_subscriber(subscriber: schemas.SubscriberCreate, db: Session = Depends(get_db)):
    return crud.create_subscriber(db=db, subscriber=subscriber)

@app.get("/subscribers/{subscriber_id}", response_model=schemas.Subscriber)
def read_subscriber(subscriber_id: int, db: Session = Depends(get_db)):
    db_subscriber = crud.get_subscriber(db, subscriber_id)
    if db_subscriber is None:
        raise HTTPException(status_code=404, detail="Subscriber not found")
    return db_subscriber

@app.get("/subscribers/", response_model=list[schemas.Subscriber])
def read_subscribers(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_subscribers(db, skip=skip, limit=limit)

# Маршруты для Connection
@app.post("/connections/", response_model=schemas.Connection)
def create_connection(connection: schemas.ConnectionCreate, db: Session = Depends(get_db)):
    return crud.create_connection(db=db, connection=connection)

@app.get("/connections/{connection_id}", response_model=schemas.Connection)
def read_connection(connection_id: int, db: Session = Depends(get_db)):
    db_connection = crud.get_connection(db, connection_id)
    if db_connection is None:
        raise HTTPException(status_code=404, detail="Connection not found")
    return db_connection

@app.get("/connections/", response_model=list[schemas.Connection])
def read_connections(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_connections(db, skip=skip, limit=limit)

@app.get("/connections/filter/", response_model=list[schemas.Connection])
def filter_connections(
    operator_id: int,
    min_debt: float = 0,
    max_debt: float = 10000,
    db: Session = Depends(get_db)
):
    return crud.filter_connections(db, operator_id, min_debt, max_debt)

@app.get("/connections/details/", response_model=list[schemas.ConnectionDetails])
def get_connection_details(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_connection_details(db, skip, limit)

@app.put("/connections/update-tariff/")
def update_tariff_plan(min_debt: float, new_tariff: str, db: Session = Depends(get_db)):
    updated_count = crud.update_tariff_plan(db, min_debt, new_tariff)
    return {"updated_connections": updated_count}

@app.get("/operators/connections-count/")
def get_connections_count(db: Session = Depends(get_db)):
    return crud.get_connections_count(db)

@app.get("/connections/sorted/", response_model=list[schemas.Connection])
def get_sorted_connections(order: str = "asc", db: Session = Depends(get_db)):
    return crud.get_sorted_connections(db, order)
@app.post("/subscribers/{subscriber_id}/add-data")
def add_json_data(subscriber_id: int, data: dict, db: Session = Depends(get_db)):
    subscriber = crud.add_json_data_to_subscriber(db, subscriber_id, data)
    if not subscriber:
        raise HTTPException(status_code=404, detail="Subscriber not found")
    return subscriber
@app.get("/subscribers/search")
def search_subscribers(query: dict, db: Session = Depends(get_db)):
    return crud.search_subscribers_by_json(db, query)

@app.get("/operators/{operator_id}/connections")
def get_connections(operator_id: int, db: Session = Depends(get_db)):
    return crud.get_connections_by_operator(db, operator_id)
