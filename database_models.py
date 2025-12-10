from sqlalchemy import Column,String,Integer,ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Todo(Base):

    __tablename__ = "todos"

    id = Column(Integer,primary_key=True,index=True)
    name = Column(String)
    priority = Column(String)
    difficulty = Column(String)
    status = Column(String)

    user_id = Column(Integer,ForeignKey("users.id"))
    user = relationship("User",back_populates="todos")

class User(Base):

    __tablename__ = "users"

    id = Column(Integer,primary_key=True,index=True)
    username = Column(String)
    password = Column(String)

    todos = relationship("Todo",back_populates="user")