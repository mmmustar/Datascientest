from fastapi import Depends, FastAPI, HTTPException, status
import requests
import pandas as pd
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from typing import Annotated, List
import sys

api = FastAPI()
security = HTTPBasic()

df = pd.read_csv("questions.csv")

users = {
    "alice": "wonderland",
    "bob": "builder",
    "clementine": "mandarine",
    "admin": "4dm1N"
}
class Question:
    def __init__(self, question: str, subject: str, use: str, correct: str, responseA: str, responseB: str, responseC: str, responseD: str, remark: str):
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

sub_list = ["BDD", "Systèmes distribués","Streaming de données", "Docker", "Classification", "Systèmes distribués", "Data Science", "Machine Learning", "Automation", "Streaming de données"]
use_list = ["Test de positionnement", "Total Bootcamp", "Test de validation"]

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

@api.get("/qcm")
def get_qcm(subjects: list[str], use: str = None,  count: int = 5, current_user: str = Depends(login)):
    for subject in subjects:
        if subject not in sub_list:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Invalid subject: {subject}")
    if use not in use_list:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid 'use' value")
    if count not in [5, 10, 20]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Number of questions must be 5, 10, or 20")
    pool =df.copy()
    if use is not None:
        pool = pool[pool['use'] == use]
    if subjects is not None:
        pool = pool[pool['subject'].isin(subjects)]
    pool = df[(df['use'] == use) & (df['subject'].isin(subjects))]
    qcm = pool.sample(n=min(len(pool), count))
    return qcm
    
@api.post("/admin")
def add_question(question : str, subject : str, use : str, correct : str,  responseA : str, responseB : str, responseC : str,responseD : str, remark : str, current_user: str = Depends(login)):
    if current_user != "admin":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Admin privileges required")
    new_question = Question(question, subject, use, correct, responseA, responseB, responseC, responseD, remark)
    question_df = pd.DataFrame([new_question.q_data()])
    question_df.to_csv("questions.csv", mode='a', header=False, index=False)
