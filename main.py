from env import API_KEY,APP_ID,SHEETY_API, SHEETY_API_2,sheet_endpoint,nutritionix_endpoint
import requests as req
from datetime import datetime as dt



# Your gender, age, weight, height
GENDER = "male"
WEIGHT_KG = 50
HEIGHT_CM = 150
AGE = 33

q = input("What exercise have you done today? \n")
params = {
    "query":q,
    "gender":GENDER,
    "age":AGE
}

headers = {
    'x-app-id':APP_ID,
    'x-app-key':API_KEY
}

# Processes the input data using NLP API
res = req.post(url=nutritionix_endpoint+"v2/natural/exercise",json=params,headers = headers)
res.raise_for_status()
results = res.json()

today_date = dt.now().strftime("%d/%m/%Y")
now_time = dt.now().strftime("%X")


# Stores the data in sheets using sheety api
for exercise in results["exercises"]:
    sheet_inputs = {
        "sheet1": {
            "date": today_date,
            "time": now_time,
            "exercise": exercise["name"].title(),
            "duration": exercise["duration_min"],
            "calories": exercise["nf_calories"]
        }
    }

    sheet_response = req.post(sheet_endpoint, json=sheet_inputs,headers={"Authorization":SHEETY_API,"Authorization": SHEETY_API_2})

    print(sheet_response.text)

