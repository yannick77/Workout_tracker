import os
from dotenv import load_dotenv
import requests
import requests_cache
import datetime as dt
requests_cache.install_cache("cache", expire_after=3600)
load_dotenv()

APP_ID = os.environ.get("APP_ID")
API_KEY = os.environ.get("API_KEY")
SHEETY_ENDPOINT = os.environ.get("SHEETY_ENDPOINT")
AUTH_KEY  = os.environ.get("AUTH_KEY")
EXERCISE_ENDPOINT = "https://app.100daysofpython.dev/v1/nutrition/natural/exercise"
GENDER = "male"
AGE = 31
WEIGHT_KG = 92
HEIGHT_CM = 171

TODAY = dt.datetime.now()
DATE = TODAY.strftime("%d/%m/%Y")
TIME = TODAY.strftime("%H:%M:%S")

"""Use Nutrition and Exercise API to format plain text"""
exercise_headers = {
    "x-app-id": APP_ID,
    "x-app-key": API_KEY,
}

exercise_input = input("Describe exercise: ")

data = {
    "query": exercise_input,
    "gender": GENDER,
    "age": AGE,
    "weight_kg": WEIGHT_KG,
    "height_cm": HEIGHT_CM,
}

response = requests.post(url=EXERCISE_ENDPOINT, headers=exercise_headers, json=data)
result = response.json()["exercises"][0]

"""Use Sheety API to enter formatted text into our google sheet"""

sheetyBody = {
    "workout": {
        "exercise": result["name"].title(),
        "duration": result["duration_min"],
        "calories": result["nf_calories"],
        "date": DATE,
        "time": TIME,
    }
}
sheetyHeader = {
    "Authorization": f"Bearer {AUTH_KEY}",
}

sheetyResponse = requests.post(url=SHEETY_ENDPOINT, json=sheetyBody, headers=sheetyHeader)
print(sheetyResponse.text)
