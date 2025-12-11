from fastapi import FastAPI,HTTPException,Depends
from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy.orm import Session

from database import engine
import database_models,models

from auth import hash_password,verify_password,create_access_token

from dependencies import use_session,get_current_user

from fastapi.security import OAuth2PasswordRequestForm

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
        #REGISTER USER
#================================ 
@app.post("/register")
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

#================================
        #LOG IN USER
#================================ 
@app.post("/login")
def login_user(form_data: OAuth2PasswordRequestForm = Depends(),
               session: Session = Depends(use_session)):
    
    db_user = session.query(database_models.User).filter(database_models.User.username==form_data.username).first()
    if not db_user:
        return {"message":"User not does not exist!"}
    if not verify_password(form_data.password,db_user.password):
        return {"message":"Incorrect password!"}

    token = create_access_token({"id":db_user.id})
    return {"access_token":token,"token_type":"bearer"}

@app.post("/signin")
def login_user(username: str,
               password: str,
               session: Session = Depends(use_session)):
    
    db_user = session.query(database_models.User).filter(database_models.User.username==username).first()
    if not db_user:
        return {"message":"User does not exist!"}
    if not verify_password(password,db_user.password):
        return {"message":"Incorrect password!"}

    token = create_access_token({"id":db_user.id})
    return {"access_token":token,"token_type":"bearer"}

#================================
        #GET ALL TODOS
#================================ 
@app.get("/todos",response_model=list[models.Todo])
def get_all_todos(current_user = Depends(get_current_user),
                  session: Session = Depends(use_session)):

    db_todos = session.query(database_models.Todo).filter(database_models.Todo.user_id==current_user.id).all()
    if db_todos == []:
        raise HTTPException(status_code=400,detail="there is no todo yet!")

    return db_todos

#================================
        #ADD TODOS
#================================ 
@app.post("/todos")
def add_todo(
            todo_input: models.Todo_Create,
            current_user = Depends(get_current_user),
            session: Session = Depends(use_session)
            ):

    new_todo = database_models.Todo(
        name = todo_input.name,
        priority = todo_input.priority,
        difficulty = todo_input.difficulty,
        status = todo_input.status,
        user_id = current_user.id
    )
    session.add(new_todo)
    session.commit()
    session.refresh(new_todo)
    return {"message":"todo added successfully!"}

