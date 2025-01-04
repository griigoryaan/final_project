from sqlalchemy import Column, Integer, String, ForeignKey, Date, DECIMAL
from sqlalchemy.orm import relationship
from app.database import Base

class Operator(Base):
    __tablename__ = "operator"

    operator_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    operator_code = Column(String(50), unique=True, nullable=False)
    number_count = Column(Integer, nullable=False)

    connections = relationship("Connection", back_populates="operator")


class Subscriber(Base):
    __tablename__ = "subscriber"

    subscriber_id = Column(Integer, primary_key=True, index=True)
    passport_data = Column(String(255), unique=True, nullable=False)
    full_name = Column(String(255), nullable=False)
    address = Column(String(255))

    connections = relationship("Connection", back_populates="subscriber")


class Connection(Base):
    __tablename__ = "connection"

    connection_id = Column(Integer, primary_key=True, index=True)
    operator_id = Column(Integer, ForeignKey("operator.operator_id", ondelete="CASCADE"))
    subscriber_id = Column(Integer, ForeignKey("subscriber.subscriber_id", ondelete="CASCADE"))
    number = Column(String(50), nullable=False)
    tariff_plan = Column(String(255))
    debt = Column(DECIMAL(10, 2), default=0)
    installation_date = Column(Date, nullable=False)

    operator = relationship("Operator", back_populates="connections")
    subscriber = relationship("Subscriber", back_populates="connections")
