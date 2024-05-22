from fastapi import FastAPI
import requests
import pandas as pd


api = FastAPI()
csv = "https://dst-de.s3.eu-west-3.amazonaws.com/fastapi_fr/questions.csv"


@api.get('/')

#chargement du csv
df = pd.read_csv(csv)





