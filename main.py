from datetime import datetime, date
from connect_sheets import connect_to_sheets
from dotenv import dotenv_values
import requests

def load_config():
    return dotenv_values(".env")

def get_user_input() -> str:
    return input("Enter your workout (e.g., 'walking 30 min'): ").strip()

def get_user_time() -> str:
    while True:
        time_input = input("Enter the time you did it (hh:mm): ").strip()
        try:
            return datetime.strptime(time_input, "%H:%M").strftime("%H:%M:%S")
        except ValueError:
            print("Invalid format. Try again (e.g., 14:30)")

def estimate_calories_burned(exercise: str, config: dict) -> dict:
    url = f"{config['HOST_DOMAIN']}{config['EXERCISE_ENDPOINT']}"
    headers = {
        "x-app-id": config["APP_ID"],
        "x-app-key": config["API_KEY"]
    }
    params = {
        "query": exercise,
        "weight_kg": config["WEIGHT_KG"],
        "height_cm": config["HEIGHT_CM"],
        "age": config["AGE"]
    }
    response = requests.post(url, headers=headers, json=params)
    return response.json()

def format_data(calories_burned: dict) -> list:
    ex = calories_burned['exercises'][0]
    return [ex['name'], ex['duration_min'], ex['nf_calories']]

def log_workout():
    config = load_config()
    raw = get_user_input()
    time_str = get_user_time()
    today = date.today().strftime("%Y-%m-%d")

    calories_burned = estimate_calories_burned(raw, config)
    exercise_data = format_data(calories_burned)

    row = [today, time_str, *exercise_data]
    sheet = connect_to_sheets()
    sheet.append_row(row)

def main():
    log_workout()

if __name__ == "__main__":
    main()