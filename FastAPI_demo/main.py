from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Define a data model for POST input
class User(BaseModel):
    name : str
    age : int 
 
# Get Endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to your own API!"}

# Dynamic path parameter
@app.get("/user/{name}")
def read_user(name:str):
    return {"message": f"Hello, {name}!"}

# POST endpoint
@app.post("/submit")
def create_user(user: User):
    return {"Message": f"{user.name} is {user.age} years old."}
