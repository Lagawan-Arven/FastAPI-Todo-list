from pydantic import BaseModel

class Todo_Create(BaseModel):
    name: str
    priority: str
    difficulty: str
    status: str

class Todo(BaseModel):
    id: int
    name: str
    priority: str
    difficulty: str
    status: str

    class Config:
        from_attributes = True

class User_Create(BaseModel):
    username: str
    password: str

class User(BaseModel):
    id: int
    username: str

    class Config:
        from_attributes = True