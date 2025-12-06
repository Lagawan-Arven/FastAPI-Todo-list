from fastapi import FastAPI,HTTPException
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

global_todo_id  = 1

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

todos: list[Todo] = []

@app.get("/todos")
def get_todos():
    if todos == []:
        return "There is no todo yet!"
    else:
        return todos

@app.get("/todos/search")
def get_searched_todos(q: str):
    searched_todos = []
    try:
        for t in todos:
            if(
                q.lower() in t.name.lower() or
                q.lower() in t.priority.lower() or
                q.lower() in t.difficulty.lower() or
                q.lower() in t.status.lower()
            ):
                searched_todos.append(t) 

        if searched_todos:
            return searched_todos
        else:
            return "Search not found!"
    except:
        return "No todo yet!"

@app.post("/todos")
def add_todo(todo_input: Todo_create):
    global global_todo_id
    todo = Todo(
        id = global_todo_id,
        name = todo_input.name,
        priority = todo_input.priority,
        difficulty = todo_input.difficulty,
        status = todo_input.status
    )

    todos.append(todo)
    auto_update_id()
    global_todo_id += 1

    return "Todo added succcessfully!"

def auto_update_id():
    local_todo_id = 1
    i = 0
    for t in todos:
        todos[i].id = local_todo_id
        i+=1
        local_todo_id+=1

@app.post("/todos/{todo_id}")
def update_todo(todo_id: int,todo_update: Todo_create):
    for t in todos:
        if t.id == todo_id:
            t.name = todo_update.name
            t.priority = todo_update.priority
            t.difficulty = todo_update.difficulty
            t.status = todo_update.status
            return "Todo updated!"
    raise HTTPException(status_code=404,detail="Todo not found!")   
        

@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int):
    for t in todos:
        if t.id == todo_id:
            todos.remove(t)
            auto_update_id()
            return "Todo deleted!"
    
    raise HTTPException(status_code=404,detail="Todo not found!")    
