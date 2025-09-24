import requests

from datetime import date, datetime
from pathlib import Path
from dotenv import load_dotenv, dotenv_values

from connect_sheets import worksheet


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

def format_data(calories_burned):
    exercise = calories_burned['exercises'][0]['name']
    duration = calories_burned['exercises'][0]['duration_min']
    calories = calories_burned['exercises'][0]['nf_calories']
    data = [exercise, duration, calories]
    return data

def main():
    env_path = Path(".env")
    load_dotenv(dotenv_path=env_path)

    config = dotenv_values(".env")

    base_url = config["HOST_DOMAIN"]
    exercise_url = config["EXERCISE_ENDPOINT"]

    today = date.today().strftime("%Y-%m-%d")

    exercise = input("Tell me which exercise you did: ")

    while True:
        exercise_time_input = input("Tell me when you did it (hh:mm): ")
        try:
            # Parse input as hh:mm
            exercise_time = datetime.strptime(exercise_time_input, "%H:%M").time()
            # Format as hh:mm:ss by adding :00 seconds
            exercise_time_str = exercise_time.strftime("%H:%M:%S")
            break
        except ValueError:
            print("Invalid format. Try again (e.g., 14:30)")

    calories_burned = estimate_calories_burned(base_url, exercise_url, exercise, config)
    exercise_data = format_data(calories_burned)  # ['Exercise', 'Duration', 'Calories']
    new_workout_entry = [today, exercise_time_str, *exercise_data]
    worksheet.append_row(new_workout_entry)

if __name__ == "__main__":
    main()