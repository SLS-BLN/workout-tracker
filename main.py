import re
from locale import normalize

import requests

from datetime import datetime, date
from connect_sheets import connect_to_sheets
from config import load_config

# --- validators and transformers ---
def is_valid_time_format(t: str) -> bool:
    return bool(re.match(r"^(?:[01]\d|2[0-3])[:.][0-5]\d$", t))

def normalize_time(time_str: str) -> str:
    return datetime.strptime(time_str, "%H:%M").strftime("%H:%M:%S")

def format_data(calories_burned: dict) -> list:
    # TODO: Validate API response structure before accessing keys
    try:
        exercises = calories_burned.get("exercises", [])
        if not exercises:
            raise ValueError("No exercises found in response.")
        ex = exercises[0]
        return [ex.get("name", "unknown"), ex.get("duration_min", 0), ex.get("nf_calories", 0)]
    except (TypeError, ValueError) as e:
        print(f"Error formatting data: {e}")
        return ["invalid", 0, 0]

def get_user_input() -> str:
    # TODO: Validate that input includes both activity and duration;
    #  note that vague input like 'run' may trigger API defaults (e.g., 'running', 30 min)
    return input("Enter your workout (e.g., 'walking 30 min'): ").strip()

def get_user_time() -> str | None:
    while True:
        time_input = input("Enter the time you did it (hh:mm or hh.mm): ").strip()
        if is_valid_time_format(time_input):
            return normalize_time(time_input)
        print("Invalid format. Try again (e.g., 14:30 or 14.30)")

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