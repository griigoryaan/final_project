from sqlalchemy.orm import Session
from app import models, schemas
from sqlalchemy.sql import func


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

def update_tariff_plan(db: Session, min_debt: float, new_tariff: str):
    updated_count = db.query(models.Connection).filter(models.Connection.debt > min_debt)\
        .update({models.Connection.tariff_plan: new_tariff})
    db.commit()
    return updated_count

def get_connections_count(db: Session):
    return db.query(models.Operator.name, func.count(models.Connection.connection_id).label("connection_count"))\
        .join(models.Connection, models.Operator.operator_id == models.Connection.operator_id)\
        .group_by(models.Operator.name).all()

def get_sorted_connections(db: Session, order: str):
    if order == "desc":
        return db.query(models.Connection).order_by(models.Connection.debt.desc()).all()
    return db.query(models.Connection).order_by(models.Connection.debt.asc()).all()

def add_json_data_to_subscriber(db: Session, subscriber_id: int, data: dict):
    subscriber = db.query(models.Subscriber).filter(models.Subscriber.subscriber_id == subscriber_id).first()
    if not subscriber:
        return None
    subscriber.additional_data = data
    db.commit()
    db.refresh(subscriber)
    return subscriber

def search_subscribers_by_json(db: Session, query: dict):
    sql_query = """
        SELECT * FROM subscriber
        WHERE additional_data::jsonb @> :query::jsonb
    """
    result = db.execute(sql_query, {"query": query}).fetchall()
    return [dict(row) for row in result]

def get_connections_by_operator(db: Session, operator_id: int):
    return (
        db.query(models.Connection)
        .filter(models.Connection.operator_id == operator_id)
        .all()
    )
