from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import os

HOST = os.environ.get('DB_HOST', 'localhost')
SQLALCHEMY_DATABASE_URL = f"postgresql://postgres:postgres@{HOST}/postgres"


engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)

SessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine
)

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    login = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)