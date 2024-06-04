import pandas as pd
import json
import requests

headers = {'User-Agent': 'ByPass'}
grandmasters = requests.get("https://api.chess.com/pub/titled/GM", headers = headers).json()
grandmasters = grandmasters["players"]
#print(len(grandmasters), "GM players")

def extract_player_info(username) :
    headers = {'User-Agent' : 'MyApp/1.0'}
    p_endpoint = "https://api.chess.com/pub/player/{}".format(username)
    p_data = requests.get(p_endpoint, headers = headers).json()
    return p_data

def get_player_stats(username):
     endpoint = "https://api.chess.com/pub/player/{}/stats".format(username)
     data = requests.get(endpoint, headers = headers).json()
     return data


gms = []
for username in grandmasters:
    gms.append(extract_player_info(username))

df_gms = df_gms.drop(["url", "is_streamer", "avatar", "@id", "verified", "location", "status", "twitch_url"], axis = 1)

countries = {}
countries_endpoint = df_gms['country'].unique()

for endpoint in countries_endpoint:
        country = requests.get(endpoint, headers = headers).json()["name"]
        countries[endpoint]= country

df_gms["country"]= df_gms['country'].replace(country)
df_gms["lastonline"] = pd.to_datetime(df_gms["lastonline"], unit='s')
df_gms["joined"] =pd.to_datetime(df_gms["joined"], unit = "s")

"\n"
df_gms.head()
df_gms.info()

print(df_gms["country"].value_count().head(5))
print(df_gms[['name','followers']].sort_values("followers", ascending = False).head(5))
print(df_gms[["name", "joined"]].dropna().sort_values("joined").head(5))