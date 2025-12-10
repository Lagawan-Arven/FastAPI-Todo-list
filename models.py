from pydantic import BaseModel

class Todo(BaseModel):
    name: str
    priority: str
    difficulty: str
    status: str

    class Config:
        from_attributes = True

class User(BaseModel):
    username: str
    password: str
    todos: list[Todo] = [] 

    class Config:
        from_attributes = True