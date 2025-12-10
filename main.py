from fastapi import FastAPI,HTTPException,Depends
from fastapi.middleware.cors import CORSMiddleware

import models
from models import Todo,User

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

#================================
        #GET A DB CONNECTION
#================================ 
def use_session():
    session = SESSION()
    try:
        yield session
    finally:
        session.close()

#================================
        #SIGN IN USER
#================================ 
@app.post("/signin")
def validate_signin(User: User,
                    session: Session = Depends(use_session)): 
    
    db_users = session.query(database_models.User).all()
    if db_users == []:
        return {"message":"no users yet"}
    for user in db_users:
        if user.username == User.username:
            if user.password == User.password:
                return {"message":"successful","user_id":user.id}
            else:
                return {"message":"incorrect password"}
    return {"message":"account does not exist"}

#================================
        #GET ALL USERS
#================================ 
@app.get("/users")
def get_users(session: Session = Depends(use_session)):

    db_users = session.query(database_models.User).all()
    if db_users == []:
        return {"message":"No user yet!"}
    else:
        return db_users

#================================
        #GET USER
#================================ 
@app.get("/users/{user_id}")
def get_user(user_id: int,
             session: Session = Depends(use_session)):

    if user_id > session.query(database_models.User).count():
        return {"message":"User not found!"}
    
    db_user = session.query(database_models.User).filter(database_models.User.id==user_id).first()
    if not db_user:
        return {"message":"user not found"}
    return db_user

#================================
        #SIGN UP USER
#================================ 
@app.post("/signup")
def add_user(User: User,
            session: Session = Depends(use_session)):

    user = database_models.User(
        username = User.username,
        password = User.password
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return {"message":"User successfully added!"}

#================================
        #GET ALL TODOS
#================================       
@app.get("/users/{user_id}/todos")
def get_todos(user_id: int,
            session: Session = Depends(use_session)):

    if user_id > session.query(database_models.User).count():
        return {"message":"User not found!"}
    
    db_todos = session.query(database_models.Todo).filter(database_models.Todo.user_id==user_id).all()
    if db_todos == []:
        return "No todo yet!"
    else:
        return db_todos


#================================
        #SEARCH TODOS
#================================ 
@app.get("/users/{user_id}/todos/search")
def get_searched_todos(user_id: int,
                       q: str,
                       session: Session = Depends(use_session)):

    if user_id > session.query(database_models.User).count():
        return {"message":"User not found!"}
    
    db_todos = session.query(database_models.Todo).filter(database_models.Todo.user_id==user_id).all()
    searched_todos = []
    try:
        for db_todo in db_todos:
            if(
                q.lower() in db_todo.name.lower() or
                q.lower() in db_todo.priority.lower() or
                q.lower() in db_todo.difficulty.lower() or
                q.lower() in db_todo.status.lower()
            ):
                searched_todos.append(db_todo) 

        if searched_todos:
            return searched_todos
        else:
            return "Search not found!"
    except:
        return "No todo yet!"
    
#================================
        #ADD TODOS
#================================ 
@app.post("/users/{user_id}/todos")
def add_todo(user_id: int,
             todo_input: Todo,
             session: Session = Depends(use_session)):

    if user_id > session.query(database_models.User).count():
        return {"message":"User not found!"}
    todo = database_models.Todo(
        name = todo_input.name,
        priority = todo_input.priority,
        difficulty = todo_input.difficulty,
        status = todo_input.status,
        user_id = user_id
    )

    session.add(todo)
    session.commit()
    session.refresh(todo)

    return {"message":"Todo added succcessfully!"}

#================================
        #UPDATE TODOS
#================================ 
@app.patch("/users/{user_id}/todos/{todo_id}")
def update_todo(user_id: int,
                todo_id: int,
                todo_update: Todo,
                session: Session = Depends(use_session)):

    if user_id > session.query(database_models.User).count():
        return {"message":"User not found!"}
    
    todo = session.query(database_models.Todo).filter(database_models.Todo.user_id==user_id,
                                                      database_models.Todo.id==todo_id).first()

    if not todo:
        raise HTTPException(status_code=404,detail="Todo not found!")   
    
    todo.name = todo_update.name
    todo.priority = todo_update.priority
    todo.difficulty = todo_update.difficulty
    todo.status = todo_update.status

    session.commit()
    session.refresh(todo)

#================================
        #DELETE TODOS
#================================       
@app.delete("/users/{user_id}/todos/{todo_id}")
def delete_todo(user_id: int,
                todo_id: int,
                session: Session = Depends(use_session)):

    if user_id > session.query(database_models.User).count():
        return {"message":"User not found!"}
     
    db_todos = session.query(database_models.Todo).filter(database_models.Todo.user_id==user_id).all()
    for db_todo in db_todos:
        if db_todo.id == todo_id:
            session.delete(db_todo)
            session.commit()
            return "Todo deleted!"
    
    raise HTTPException(status_code=404,detail="Todo not found!")    
