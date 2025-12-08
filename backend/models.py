
from pydantic import BaseModel

class Todo_create(BaseModel):
    name: str
    priority: str
    difficulty: str
    status: str