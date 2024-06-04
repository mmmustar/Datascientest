from fastapi import Depends, FastAPI, HTTPException, status, Query
import pandas as pd
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from typing import Annotated, Optional
import random
from random import sample
import warnings

api = FastAPI()
security = HTTPBasic()

users = {
    "alice": "wonderland",
    "bob": "builder",
    "clementine": "mandarine",
    "admin": "4dm1N"
}
class Question:
    def __init__(
            self, question: str,
            subject: Annotated[str, "Type subject category"],
            use: Annotated[str, "Type use category"],
            correct: Annotated[str, "Type correct answers (A, B, C, D)"],
            responseA: Annotated[str, "Type answer A"],
            responseB: Annotated[str, "Type answer B"],
            responseC: Annotated[str, "Type answer B not mandatory"],
            responseD: Annotated[str, "Type answer D not mandatory"],
            remark: Annotated[str, "Type any remark"],
            ):
        self.question = question
        self.subject = subject
        self.use = use
        self.correct = correct
        self.responseA = responseA
        self.responseB = responseB
        self.responseC = responseC
        self.responseD = responseD
        self.remark = remark
    
    def q_data(self):
        return {
            "question": self.question,
            "subject": self.subject,
            "use": self.use,
            "correct": self.correct,
            "responseA": self.responseA,
            "responseB": self.responseB,
            "responseC": self.responseC,
            "responseD": self.responseD,
            "remark": self.remark,
        }

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

@api.get("/")
def running():
    return "API OK"

@api.get("/admin")
def add_question(
    question : Annotated[str, "Type question text"],
    subject : Annotated[str, "Type subject category"],
    use : Annotated[str, "Type use category"],
    correct : Annotated[str, "Type correct answers (A, B, C, D)"],
    responseA : Annotated[str, "Type answer A"],
    responseB : Annotated[str, "Type answer B"] = None,
    responseC : Annotated[str, "Type answer B not mandatory"] = None,
    responseD: Annotated[str, "Type answer D not mandatory"] = None,
    remark: Annotated[str, "Type any remark"] = None ,
    current_user: str = Depends(login)
    ):
     
    if current_user != "admin":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Admin privileges required")
    new_question = Question(question, subject, use, correct, responseA, responseB, responseC, responseD, remark)
    question_df = pd.DataFrame([new_question.q_data()])
    question_df.to_csv("questions.csv", mode='a', header=False, index=False)
    return  {"message": "question added successfully"}


@api.get("/qcm")
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