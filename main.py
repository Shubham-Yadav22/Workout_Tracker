import requests
import datetime as dt
import os

today_date = dt.datetime.today().date()
today_date = today_date.strftime("%d/%m/%Y")
today_time = dt.datetime.now().time()
today_time_str = today_time.strftime("%X")

Sheety_Url = os.environ['SHEET_ENDPOINT']

USERNAME = os.environ["USERNAME"]
PASSWORD = os.environ["PASSWORD"]
My_AUTHORIZATION_HEADER = os.environ["TOKEN"]


My_Age = 19
My_weight = 50.3
My_gender = "male"
My_height = 165

API_ID = os.environ["APP_ID"]
API_KEY = os.environ["API_KEY"]

Exercise_endpoint = "https://trackapi.nutritionix.com/v2/natural/exercise"

headers = {
    "x-app-id": API_ID,
    "x-app-key": API_KEY,
    "Content-Type": "application/json"
}

exercise = input("Tell me which exercise did you perform? ")

exercise_params = {
    "query": exercise,
    "gender": My_gender,
    "weight_kg": My_weight,
    "height_cm": My_height,
    "age": My_Age
}

response = requests.post(url=Exercise_endpoint, headers=headers, json=exercise_params)


if response.status_code == 200:
    result = response.json()
    data = result['exercises'][0]

    Exercise = data['user_input']
    Duration = data['duration_min']
    Calories = data['nf_calories']

    auth_header_sheety = {
        "Authorization": My_AUTHORIZATION_HEADER
    }

    for exercise in result["exercises"]:
        sheet_inputs = {
            "workout": {
                "date": today_date,
                "time": today_time_str,
                "exercise": exercise["name"].title(),
                "duration": exercise["duration_min"],
                "calories": exercise["nf_calories"]
            }

        }

        sheety_response = requests.post(Sheety_Url, json=sheet_inputs, headers=auth_header_sheety)

