from sqlalchemy.orm import Session
from app import models, schemas

# CRUD для Operator
def create_operator(db: Session, operator: schemas.OperatorCreate):
    db_operator = models.Operator(**operator.dict())
    db.add(db_operator)
    db.commit()
    db.refresh(db_operator)
    return db_operator

def get_operator(db: Session, operator_id: int):
    return db.query(models.Operator).filter(models.Operator.operator_id == operator_id).first()

def get_operators(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Operator).offset(skip).limit(limit).all()

def delete_operator(db: Session, operator_id: int):
    db_operator = get_operator(db, operator_id)
    if db_operator:
        db.delete(db_operator)
        db.commit()
    return db_operator

# CRUD для Subscriber
def create_subscriber(db: Session, subscriber: schemas.SubscriberCreate):
    db_subscriber = models.Subscriber(**subscriber.dict())
    db.add(db_subscriber)
    db.commit()
    db.refresh(db_subscriber)
    return db_subscriber

def get_subscriber(db: Session, subscriber_id: int):
    return db.query(models.Subscriber).filter(models.Subscriber.subscriber_id == subscriber_id).first()

def get_subscribers(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Subscriber).offset(skip).limit(limit).all()

# CRUD для Connection
def create_connection(db: Session, connection: schemas.ConnectionCreate):
    db_connection = models.Connection(**connection.dict())
    db.add(db_connection)
    db.commit()
    db.refresh(db_connection)
    return db_connection

def get_connection(db: Session, connection_id: int):
    return db.query(models.Connection).filter(models.Connection.connection_id == connection_id).first()

def get_connections(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Connection).offset(skip).limit(limit).all()

def filter_connections(db: Session, operator_id: int, min_debt: float, max_debt: float):
    return db.query(models.Connection).filter(
        models.Connection.operator_id == operator_id,
        models.Connection.debt >= min_debt,
        models.Connection.debt <= max_debt
    ).all()

def get_connection_details(db: Session, skip: int, limit: int):
    return db.query(
        models.Connection,
        models.Operator.name.label("operator_name"),
        models.Subscriber.full_name.label("subscriber_name")
    ).join(models.Operator, models.Connection.operator_id == models.Operator.operator_id)\
     .join(models.Subscriber, models.Connection.subscriber_id == models.Subscriber.subscriber_id)\
     .offset(skip).limit(limit).all()
