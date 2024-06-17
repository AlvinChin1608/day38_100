import requests
import os
from dotenv import load_dotenv
from datetime import datetime

# Load environment variable from the .env file
load_dotenv("./vars/.env")

NUTRI_ID = os.getenv("APP_ID")
NUTRI_AUTH = os.getenv("APP_API_KEY")

NUTRI_ENDPOINT = "https://trackapi.nutritionix.com/v2/natural/exercise"
SHEETY_ENDPOINT = os.getenv("SHEETY_API")

# make it update my age automatically
current_age = int(datetime.now().strftime("%Y")) - 1995

# your information
GENDER = "male"
WEIGHT_KG = 60
HEIGHT_CM = 180
AGE = current_age

exercise_text = input("Tell me which exercise you did: ")

# https://trackapi.nutritionix.com/docs/#/default/post_v2_natural_exercise
# Parameters for the API request
nutri_params = {
    "query": exercise_text,
    "gender": GENDER,
    "weight_kg": WEIGHT_KG,
    "height_cm": HEIGHT_CM,
    "age": AGE,
}

headers = {
    "x-app-id": NUTRI_ID,
    "x-app-key": NUTRI_AUTH,
}

response = requests.post(url=NUTRI_ENDPOINT, json=nutri_params, headers=headers)
response.raise_for_status()
result = response.json()["exercises"]
print(result)

today_date = datetime.now().strftime("%d/%m/%Y")
now_time = datetime.now().strftime("%X")

for workout in result:
    sheet_input = {
        "workout": {
            "date": today_date,
            "time": now_time,
            "exercise": workout['user_input'].title(),
            "duration": workout['duration_min'],
            "calories": workout['nf_calories'],
        }
    }
    sheet_response = requests.post(SHEETY_ENDPOINT, json=sheet_input)
    sheet_response.raise_for_status()
    print(sheet_response.text)

# Google sheet https://docs.google.com/spreadsheets/d/1rgBJKPmaAUTkkfHXzBUAJGCcOV5NR7h3nzK6iAhWfmQ/edit?usp=sharing
