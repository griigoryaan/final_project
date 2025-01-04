from pydantic import BaseModel
from typing import Optional

# Схемы для Operator
class OperatorBase(BaseModel):
    name: str
    operator_code: str
    number_count: int

class OperatorCreate(OperatorBase):
    pass

class Operator(OperatorBase):
    operator_id: int

    class Config:
        orm_mode = True

# Схемы для Subscriber
class SubscriberBase(BaseModel):
    passport_data: str
    full_name: str
    address: Optional[str]

class SubscriberCreate(SubscriberBase):
    pass

class Subscriber(SubscriberBase):
    subscriber_id: int

    class Config:
        orm_mode = True

# Схемы для Connection
class ConnectionBase(BaseModel):
    operator_id: int
    subscriber_id: int
    number: str
    tariff_plan: Optional[str]
    debt: Optional[float] = 0
    installation_date: str

class ConnectionCreate(ConnectionBase):
    pass

class Connection(ConnectionBase):
    connection_id: int

    class Config:
        orm_mode = True
