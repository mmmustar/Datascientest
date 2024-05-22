from fastapi import Depends, FastAPI, HTTPException, status
import requests
import pandas as pd
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from typing import Annotated

api = FastAPI()

url = "https://dst-de.s3.eu-west-3.amazonaws.com/fastapi_fr/questions.csv"
csv = requests.get(url)
csv.raise_for_status()
df = pd.read_csv(csv)


#a ameliorer en éliminant les if et elifs mais simple a lire
def filter(use: str= None, subjects: str= None):
    if use == None and subjects != None:
        db = (df["subjects"] == subjects)
    elif use != None and subjects == None:
        db = (df["use"] == use )
    elif use == None and subjects == None:
        db = df
    else:
        db = (df['use'] == use) | (df['subjects'] == subjects)
    return db

security = HTTPBasic()

users = {
    "alice": "wonderland",
    "bob": "builder",
    "clementine": "mandarine"
}

def login(credentials: Annotated[HTTPBasicCredentials, Depends(security)],):
    current_username = credentials.username
    current_password = credentials.password
    if current_username not in users or users[current_username] != current_password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return "Welcome ", current_username 

@api.get("/")
def running():
    return "API OK"

@api.post("/login")
def ok(credentials: Annotated[HTTPBasicCredentials, Depends(security)]):
    return login(credentials)

@api.get_qcm("/questions")
def get_questions(use: str = None, subjects: str = None, count: int = 5,credentials: HTTPBasicCredentials = Depends(security)):
    login(credentials)
    if count not in [5, 10, 20]:
        raise ValueError("Invalid 'count' value. Must be 5, 10, or 20.")
    db = []
    filter(use, subjects)
    qcm = db.sample(n=count, replace=False)
    print (qcm)












