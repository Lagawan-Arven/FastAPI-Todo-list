
from pydantic import BaseModel

class Todo(BaseModel):
    id: int
    name: str
    priority: str
    difficulty: str
    status: str

class Todo_create(BaseModel):
    name: str
    priority: str
    difficulty: str
    status: str