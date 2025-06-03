from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker, scoped_session
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from contextlib import contextmanager

engine = create_engine("sqlite:///backend/database.db", echo=False)
Base = declarative_base()
SessionFactory = sessionmaker(bind=engine)
Session = scoped_session(SessionFactory)

@contextmanager
def get_session():
    db = Session()
    try:
        yield db
        db.commit()
    except:
        db.rollback()
        raise
    finally:
        db.close()


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    login = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(String, default="employee")  # admin или employee
    telegram_id = Column(String, unique=True, nullable=True)
    balance = Column(Float, default=0.0)

    sessions = relationship("SessionLog", back_populates="user")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class PC(Base):
    __tablename__ = "pcs"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    ip_address = Column(String)
    mac_address = Column(String)
    is_online = Column(Boolean, default=False)
    in_use = Column(Boolean, default=False)
    pos_x = Column(Integer, default=0)
    pos_y = Column(Integer, default=0)


    sessions = relationship("SessionLog", backref="pc")


class SessionLog(Base):
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

    product = relationship("Product")
    user = relationship("User")
