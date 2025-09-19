import requests

from pathlib import Path
from dotenv import load_dotenv, dotenv_values

def estimate_calories_burned(base_url, exercise_url, exercise, config):
    url = f"{base_url}{exercise_url}"

    header = {
        "x-app-id": config["APP_ID"],
        "x-app-key": config["API_KEY"]
    }

    params = {
        "query": exercise,
        "weight_kg": config["WEIGHT_KG"],
        "height_cm": config["HEIGHT_CM"],
        "age": config["AGE"]
    }

    calories = requests.post(url, headers=header, json=params)
    return calories.json()

def main():
    env_path = Path(".env")
    load_dotenv(dotenv_path=env_path)

    config = dotenv_values(".env")

    base_url = config["HOST_DOMAIN"]
    exercise_url = config["EXERCISE_ENDPOINT"]

    exercise = input("Tell me which exercise you did: ")

    calories_burned = estimate_calories_burned(base_url, exercise_url, exercise, config)
    print(calories_burned)

if __name__ == "__main__":
    main()