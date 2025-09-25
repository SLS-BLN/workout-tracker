```markdown
# 🏋️‍♂️ Workout Tracker

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Last Commit](https://img.shields.io/github/last-commit/SLS-BLN/workout-tracker)](https://github.com/SLS-BLN/workout-tracker/commits/main)
[![Issues](https://img.shields.io/github/issues/SLS-BLN/workout-tracker)](https://github.com/SLS-BLN/workout-tracker/issues)
[![Stars](https://img.shields.io/github/stars/SLS-BLN/workout-tracker?style=social)](https://github.com/SLS-BLN/workout-tracker/stargazers)

Track your workouts with structured logging, calorie estimation, and Google Sheets integration. This project is designed for learning—not production—and focuses on connecting APIs, managing credentials, and building modular workflows.

## 🚀 Features

- Manual workout input with time (`hh:mm`) via CLI  
- Calorie estimation using Nutritionix API  
- Secure logging to Google Sheets via service account  
- `.env`-driven configuration for credentials and sheet ID  
- Modular architecture: input, API, formatting, and logging separated  

## 📦 Setup

### 1. Clone the repo

```bash
git clone https://github.com/SLS-BLN/workout-tracker.git
cd workout-tracker
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Create `.env`

```ini
# .env
APP_ID=your_nutritionix_app_id
API_KEY=your_nutritionix_api_key
HOST_DOMAIN=https://trackapi.nutritionix.com
EXERCISE_ENDPOINT=/v2/natural/exercise
WEIGHT_KG=70
HEIGHT_CM=175
AGE=30
SPREADSHEET_ID=your_google_sheet_id
WORKSHEET_NAME=Sheet1
```

### 4. Add your service account key

Place your `service_account_key.json` inside the `secrets/` folder:

```
secrets/service_account_key.json
```

## 🧠 Usage

```bash
python main.py
```

You’ll be prompted to enter:

- Your workout (e.g., `walking 30 min`)
- The time you did it (`hh:mm`)

The script will:

- Estimate calories via Nutritionix  
- Log `[Date, Time, Exercise, Duration, Calories]` to your Google Sheet  

## 🛠 Architecture

| Module             | Responsibility                              |
|--------------------|----------------------------------------------|
| `main.py`          | Orchestrates input, API call, formatting, logging |
| `connect_sheets.py`| Authenticates and connects to Google Sheets |
| `.env`             | Stores credentials and config                |

## ✅ Example Output in Sheet

```
Date        | Time     | Exercise | Duration | Calories
--------------------------------------------------------
2025-09-24  | 14:30:00 | walking  | 30       | 185.5
```

## 🔐 Security Notes

- Credentials are loaded via `.env` and never hardcoded  
- Service account key is isolated in `secrets/`  
- No sensitive data is exposed in logs or commits  

## 🧩 TODOs (Learning-Oriented)

This project is intentionally minimal and focused on API integration. Future improvements could include:

- [ ] Validate workout input (e.g., reject empty or malformed strings)
- [ ] Validate time input (e.g., reject out-of-range values like `99:99`)
- [ ] Handle Nutritionix API errors gracefully (e.g., empty response, rate limits)
- [ ] Add retry logic for failed API calls
- [ ] Add a `--dry-run` mode for debugging without writing to Sheets
- [ ] Log raw input alongside parsed data for traceability
- [ ] Add unit tests for each module
- [ ] Add support for multiple worksheets or sheet tabs
- [ ] Add optional logging to local file for offline tracking
```