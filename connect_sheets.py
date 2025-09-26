import gspread
from config import load_config

def connect_to_sheets(creds_path: str = "secrets/service_account_key.json") -> gspread.Worksheet:
    """Connect to a Google Sheets worksheet using service account credentials."""
    config = load_config()

    # Google Sheets API Access Method:
    # - Two options: access by spreadsheet title or by spreadsheet ID
    # - Title-based access appears logical but is unreliable (can cause 402 errors)
    # - ID-based access is foolproof and works consistently
    # - Spreadsheet ID is found in the URL: docs.google.com/spreadsheets/d/[ID]/edit
    # - Always use ID for production stability
    spreadsheet_id = config.get("SPREADSHEET_ID")
    worksheet_name = config.get("WORKSHEET_NAME", "Sheet1")

    if not spreadsheet_id:
        raise ValueError("Missing required key 'SPREADSHEET_ID' in .env")

    try:
        gc = gspread.service_account(filename=creds_path)
    except FileNotFoundError:
        raise FileNotFoundError(f"Service account key not found at '{creds_path}'")
    except Exception as e:
        raise RuntimeError(f"Failed to load service account credentials: {e}")

    try:
        spreadsheet = gc.open_by_key(spreadsheet_id)
    except gspread.exceptions.SpreadsheetNotFound:
        raise ValueError(f"Spreadsheet with ID '{spreadsheet_id}' not found or inaccessible")

    try:
        worksheet = spreadsheet.worksheet(worksheet_name)
    except gspread.exceptions.WorksheetNotFound:
        raise ValueError(f"Worksheet '{worksheet_name}' not found in spreadsheet '{spreadsheet_id}'")

    return worksheet