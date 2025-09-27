import gspread
from config import load_config

credentials_path = "secrets/service_account_key.json"

def create_service_account_client(creds_path: str):
    try:
        gc = gspread.service_account(filename=creds_path)
        return gc
    except FileNotFoundError:
        raise FileNotFoundError(f"Service account key not found at '{creds_path}'")
    except Exception as e:
        raise RuntimeError(f"Failed to load service account credentials: {e}")

def open_spreadsheet_by_id(gc, spreadsheet_id: str):
    try:
        spreadsheet = gc.open_by_key(spreadsheet_id)
        return spreadsheet
    except gspread.exceptions.SpreadsheetNotFound:
        raise ValueError(f"Spreadsheet with ID '{spreadsheet_id}' not found or inaccessible")

def get_worksheet(spreadsheet: gspread.Spreadsheet, worksheet_name: str):
    try:
        worksheet = spreadsheet.worksheet(worksheet_name)
        return worksheet
    except gspread.exceptions.WorksheetNotFound:
        raise ValueError(f"Worksheet '{worksheet_name}' not found")


def connect_to_sheets() -> gspread.Worksheet:
    """Connect to a Google Sheets worksheet using service account credentials.
        This is the main entry point for Google Sheets access. It handles the complete
        workflow: authentication -> spreadsheet access -> worksheet selection.
        """
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

    gc = create_service_account_client(credentials_path)
    spreadsheet = open_spreadsheet_by_id(gc, spreadsheet_id)
    worksheet = get_worksheet(spreadsheet, worksheet_name)

    return worksheet