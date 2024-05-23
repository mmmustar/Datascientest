from fastapi import Depends, FastAPI, HTTPException, status
import requests
import pandas as pd
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from typing import Annotated
import sys

api = FastAPI()
security = HTTPBasic()

#url = "https://dst-de.s3.eu-west-3.amazonaws.com/fastapi_fr/questions.csv"
#csv = requests.get("https://dst-de.s3.eu-west-3.amazonaws.com/fastapi_fr/questions.csv")
#csv.raise_for_status()
csv = "questions.csv"
df = pd.read_csv(csv)

users = {
    "alice": "wonderland",
    "bob": "builder",
    "clementine": "mandarine",
    "admin": "4dm1N"
}

#y a t'il plus simple ?
def filter(use: str= None, subjects: list= None):
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

#semble être la seule chose qui fonctionne comme je m'y attendais
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

#je ne suis pas sur que ca fonctionne comme souhaité (comment le verifier)
def quizz(DataFrame, count : int):
    score = 0
    pool ={"responseA", "responseB", "responseC", "reponseD"}
    for i in range(count):
        print(DataFrame["questions"][i])
        for col in pool:
            if DataFrame[col][i].notnull():
                print((pool[-1]), " : " ,DataFrame[col][i])
        answer = input("réponse (indiquez la ou les lettres correspondantes): ")
        if sorted(set(answer.replace(',', ''))) == sorted(set(DataFrame["correct"][i].replace(',', ''))):
            score += 1
        print (DataFrame["correct"][i])    
    return score

@api.get("/")
def running():
    return "API OK"

@api.post("/login")
def ok(credentials: Annotated[HTTPBasicCredentials, Depends(security)]):
    return login(credentials)

#comment verifier
@api.get("/questions")
def get_questions(use: str = None, subjects: list = None, count: int = 5,credentials: HTTPBasicCredentials = Depends(security)):
    login(credentials)
    if count not in [5, 10, 20]:
        raise ValueError("Invalid 'count' value. Must be 5, 10, or 20.")
    db = filter(use, subjects)
    qcm = db.sample(n=count, replace=False)
    score = quizz(qcm, count)    
    print(score)

#c'est lourd
@api.put("/admin")
def add_question(credentials: HTTPBasicCredentials = Depends(security)):
    question_data ={"question": "", "subject": "", "use": "", "correct": "","responseA": "","responseB": "", "responseC": "", "responseD": "", "remark": ""}
    if login(credentials) != "admin":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Admin privileges required")
    question_data["subject"] = input("Indiquez le sujet: ")
    question_data["use"] = input("Indiquez le type de la question: ")
    question_data["question"] = input("Tappez la question a ajouter: ")
    question_data["reponseA"] = input("Indiquez la proposition de réponse A: ")
    question_data["reponseB"] = input("Indiquez la proposition de réponse B: ")
    question_data["reponseC"] = input("Indiquez la proposition de réponse C: ")
    question_data["reponseD"] = input("Indiquez la proposition de réponse D: ")
    question_data["correct"] = input("Indiquez les bonnes réponses: ")
    question_data["remark"] = input("Indiquez d'enventuelles remarques: ")
    question_df = pd.DataFrame([question_data])
    question_df.to_csv("your_file.csv", mode='a', header=False, index=False)
    print("question ajoutée")








