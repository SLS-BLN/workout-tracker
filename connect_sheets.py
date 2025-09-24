import gspread
from dotenv import dotenv_values

def load_config(path=".env") -> dict:
    config = dotenv_values(path)
    if "SPREADSHEET_ID" not in config:
        raise ValueError("Missing SPREADSHEET_ID in .env")
    return config

def connect_to_sheets(creds_path: str = "secrets/service_account_key.json") -> gspread.Worksheet:
    config = load_config()
    spreadsheet_id = config["SPREADSHEET_ID"]
    worksheet_name = config.get("WORKSHEET_NAME", "Sheet1")

    try:
        gc = gspread.service_account(filename=creds_path)
        spreadsheet = gc.open_by_key(spreadsheet_id)
        worksheet = spreadsheet.worksheet(worksheet_name)
        return worksheet
    except FileNotFoundError:
        raise FileNotFoundError(f"Service account key not found at '{creds_path}'")
    except gspread.exceptions.WorksheetNotFound:
        raise ValueError(f"Worksheet '{worksheet_name}' not found in spreadsheet '{spreadsheet_id}'")
    except Exception as e:
        raise RuntimeError(f"Failed to connect to Google Sheets: {e}")