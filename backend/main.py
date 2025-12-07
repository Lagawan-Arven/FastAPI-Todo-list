from fastapi import FastAPI,HTTPException,Depends
from fastapi.middleware.cors import CORSMiddleware
from models import Todo,Todo_create
from sqlalchemy.orm import Session
from database import SESSION,engine
import database_models

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"]
)

database_models.Base.metadata.create_all(bind=engine)

def use_session():
    session = SESSION()
    try:
        yield session
    finally:
        session.close()

def get_all_todos():
    session = SESSION()
    db_todos = session.query(database_models.Todo).all()
    session.close()
    return db_todos

@app.get("/todos")
def get_todos(session: Session = Depends(use_session)):
    db_todos = session.query(database_models.Todo).all()
    if db_todos == []:
        return "No todo yet!"
    else:
        return db_todos

@app.get("/todos/search")
def get_searched_todos(q: str,session: Session = Depends(use_session)):
    todos = get_all_todos()
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
def add_todo(todo_input: Todo_create,session: Session = Depends(use_session)):
    todo = database_models.Todo(
        name = todo_input.name,
        priority = todo_input.priority,
        difficulty = todo_input.difficulty,
        status = todo_input.status
    )

    session.add(todo)
    session.commit()
    session.refresh(todo)

    return "Todo added succcessfully!"

@app.post("/todos/{todo_id}")
def update_todo(todo_id: int,
                todo_update: Todo_create,
                session: Session = Depends(use_session)):

    todo = session.query(database_models.Todo).filter(database_models.Todo.id==todo_id).first()

    if not todo:
        raise HTTPException(status_code=404,detail="Todo not found!")   
    
    todo.name = todo_update.name
    todo.priority = todo_update.priority
    todo.difficulty = todo_update.difficulty
    todo.status = todo_update.status

    session.commit()
    session.refresh(todo)
        
@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int,session: Session = Depends(use_session)):
    todos = get_all_todos()
    for t in todos:
        if t.id == todo_id:
            session.delete(t)
            session.commit()
            return "Todo deleted!"
    
    raise HTTPException(status_code=404,detail="Todo not found!")    
