# backend/models.py
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from datetime import datetime

engine = create_engine("sqlite:///backend/database.db", echo=False)
Base = declarative_base()
SessionLocal = sessionmaker(bind=engine)


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    telegram_id = Column(String, unique=True, nullable=True)
    balance = Column(Float, default=0.0)

    sessions = relationship("Session", back_populates="user")


class PC(Base):
    __tablename__ = "pcs"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    ip_address = Column(String)
    mac_address = Column(String)
    is_online = Column(Boolean, default=False)
    in_use = Column(Boolean, default=False)


class Session(Base):
    __tablename__ = "sessions"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    pc_id = Column(Integer, ForeignKey("pcs.id"))
    start_time = Column(DateTime, default=datetime.utcnow)
    end_time = Column(DateTime, nullable=True)
    cost = Column(Float, default=0.0)

    user = relationship("User", back_populates="sessions")


class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    price = Column(Float)
    category = Column(String)  # Еда, напитки, аксессуары и т.п.


class Sale(Base):
    __tablename__ = "sales"
    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    quantity = Column(Integer, default=1)
    total_price = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)
