import json
import random
import warnings
from typing import Annotated

import pandas as pd
from fastapi import Depends, FastAPI, HTTPException, Query, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel

app = FastAPI()
security = HTTPBasic()

users = {
    "alice": "wonderland",
    "bob": "builder",
    "clementine": "mandarine",
    "admin": "4dm1N"
}

class Question(BaseModel):
    question: str
    subject: str
    use: str
    correct: str
    responseA: str
    responseB: str
    responseC: str
    responseD: str
    remark: str

use_list = ["Test de positionnement", "Total Bootcamp", "Test de validation"]
sub_list = ["BDD", "Systèmes distribués", "Streaming de données", "Docker", "Classification", "Data Science", "Machine Learning", "Automation"]

def login(credentials: Annotated[HTTPBasicCredentials, Depends(security)],):
    current_username = credentials.username
    current_password = credentials.password

    if current_username not in users or users[current_username] != current_password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )

    return current_username

@app.get("/")
def running():
    return "API OK"

@app.post("/admin")
def add_question(question : Question, current_user: str = Depends(login)):
    if current_user != "admin":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Admin privileges required")

    question_df = pd.DataFrame([json.dumps(question.__dict__)])
    question_df.to_csv("questions.csv", mode='a', header=False, index=False)

    return  {"message": "question added successfully"}


@app.get("/qcm")
def qcm_gen(
    use: str = Query(None, description="Possible Values : 'Test de positionnement', 'Total Bootcamp', or 'Test de validation'"),
    subjects: list[str] = Query(None, description="Possible values can be one or multiple of 'BDD', 'Systèmes distribués', 'Streaming de données', 'Docker', 'Classification', 'Data Science', 'Machine Learning', 'Automation'"),
    count: int = Query(5, description="Available values 5, 10 or 20"),
    current_user: str = Depends(login)
):
    if count not in {5, 10, 20}:
        raise HTTPException(status_code=400, detail="Available values for count are 5, 10, or 20")
    df = pd.read_csv("questions.csv")
    df = df.fillna("")
    if use and use not in use_list:
        raise HTTPException(status_code=400, detail="Invalid use value. : 'Test de positionnement', 'Total Bootcamp', or 'Test de validation'")

    if subjects:
        for subject in subjects:
            if subject not in sub_list:
                raise HTTPException(status_code=400, detail="Invalid subject. Possible values can be one or multiple of 'BDD', 'Systèmes distribués', 'Streaming de données', 'Docker', 'Classification', 'Data Science', 'Machine Learning', 'Automation'")

    if use:
        df = df[df['use'] == use]

    if subjects:
        df = df[df['subject'].isin(subjects)]

    if len(df) < 5:
        raise HTTPException(status_code=400, detail="Question pool is too short. Please change parameters.")

    if len(df) < count:
        warnings.warn("Question pool is too short. All available questions are being provided.")
        count = len(df)

    df_index = random.sample(list(df.index),count)
    qcm = df.loc[df_index]

    return  qcm