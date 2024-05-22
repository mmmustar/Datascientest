from fastapi import FastAPI
import requests
import pandas as pd
import sys

api = FastAPI()
@api.get("/")
def running():
    return print("API OK")

users = {
    "alice": "wonderland",
    "bob": "builder",
    "clementine": "mandarine"
}

@api.post("/login")
def login(username: str, password: str):
    if username in users and users[username] == password:
        return {"message": "Login OK"}
    else:
        return {"message": "Erreur d'identification"}





