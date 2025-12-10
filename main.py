from fastapi import FastAPI,HTTPException,Depends
from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy.orm import Session

from database import SESSION,engine
import database_models,models

from auth import hash_password,verify_password

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

fake_session = {}

def get_current_user(username: str):
    if username not in fake_session:
        return {"message":"Not logged in!"}
    return username

@app.post("/register",response_model=models.User)
def add_user(user_input: models.User_Create,
             session: Session = Depends(use_session)):
    
    #check if user already exist
    if session.query(database_models.User).filter(database_models.User.username==user_input.username).first():
        return {"message":"user already existed!"}
    
    hashed_password = hash_password(user_input.password)
    new_user = database_models.User(
        username = user_input.username,
        password = hashed_password
    )
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return {"message":"user added successfully!"}

@app.post("/login")
def login_user(username: str,
               password: str,
               session: Session = Depends(use_session)):
    
    db_user = session.query(database_models.User).filter(database_models.User.username==username).first()
    if not db_user:
        return {"message":"User not does not exist!"}
    if not verify_password(password,db_user.password):
        return {"message":"Incorrect password!"}
    
    fake_session[username] = True

    return {"message":"user login successfull!"}

@app.get("/todos",response_model=list[models.Todo])
def get_all_todos(username: str,
                  session: Session = Depends(use_session)):
    
    get_current_user(username)

    db_user = session.query(database_models.User).filter(database_models.User.username==username).first()

    db_todos = session.query(database_models.Todo).filter(database_models.Todo.user_id==db_user.id).all()

    return db_todos

@app.post("todos",response_model=models.Todo)
def add_todo(username: str,
             todo_input: models.Todo_Create,
             session: Session = Depends(use_session)):
    
    get_current_user(username)

    db_user = session.query(database_models.User).filter(database_models.User.username==username).first()
    new_todo = database_models.Todo(
        name = todo_input.name,
        priority = todo_input.priority,
        difficulty = todo_input.difficulty,
        status = todo_input.status,
        user_id = db_user.id
    )
    session.add(new_todo)
    session.commit()
    session.refresh(new_todo)
    return {"message":"todo added successfully!"}

