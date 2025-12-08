from sqlalchemy import Column,String,Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Todo(Base):

    __tablename__ = "Todos"

    id = Column(Integer,primary_key=True,index=True)
    name = Column(String)
    priority = Column(String)
    difficulty = Column(String)
    status = Column(String)

class User(Base):

    __tablename__ = "Test_Users"

    user_id = Column(Integer,primary_key=True,index=True)
    username = Column(String)
    password = Column(String)