from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"]
)

class Todo(BaseModel):
    name: str
    priority: str
    difficulty: str
    status: str

todos: list[Todo] = []

@app.get("/todos")
def get_todos():
    return todos

@app.post("/todos")
def add_todo(todo: Todo):
    todos.append(todo)
    return {"message":"todo added succcessfully!"}

@app.delete("/todos/{todo_name}")
def delete_todo(todo_name: str):
    for t in todos:
        if t.name == todo_name:
            todos.remove(t)
            return {"message":"todo deleted!"}