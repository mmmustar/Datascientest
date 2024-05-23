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

def filter(subjects,use):
    db = []
    if use is None and subjects is not None:
        db = df[df["subjects"].isin(subjects)]
    elif use is not None and subjects is None:
        db = (df["use"] == use )
    elif use is None and subjects is None:
        db = df
    else:
        db = df[(df['use'] == use) & (df['subjects'].isin(subjects))]
    return db

@api.get("/")
def running():
    return "API OK"

@api.post("/questions")
def do_qcm(subjects: list = None, use: str = None, count: int = 5):
    if count not in [5, 10, 20]:
        raise ValueError("Invalid 'count' value. Must be 5, 10, or 20.")
    if use is not None and use not in use_list:
        raise ValueError("Invalid value for 'use'. Available values are : Test de positionnement, Total Bootcamp,  Test de validation")
    if subjects is not None and any (subject not in sub_list for subject in subjects):
        raise ValueError("Invalid value for 'subjects'. Available values are BDD, Systèmes distribués, Streaming de données, Docker, Classification, Systèmes distribués, Data Science, Machine Learning, Automation, Streaming de données")
    db = filter(subjects, use)
    qcm = db.sample(n=count, replace=False)
    return qcm

@api.get("/admin")
def add_question(question : str, subject : str, use : str, correct : str,  responseA : str, responseB : str, responseC : str,responseD : str, remark : str, current_user: str = Depends(login)):
    if current_user != "admin":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Admin privileges required")
    new_question = Question(question, subject, use, correct, responseA, responseB, responseC, responseD, remark)
    question_df = pd.DataFrame([new_question.q_data()])
    question_df.to_csv("questions.csv", mode='a', header=False, index=False)
