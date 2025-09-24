import gspread

from google.oauth2.service_account import Credentials
from pathlib import Path
from dotenv import load_dotenv, dotenv_values

env_path = Path(".env")
load_dotenv(dotenv_path=env_path)
spreadsheet_id = dotenv_values(".env")["SPREADSHEET_ID"]
worksheet_name = dotenv_values(".env")["WORKSHEET_NAME"]

# --- Configuration ---
# The path to your service account key file within the 'secrets' folder
SERVICE_ACCOUNT_FILE = 'secrets/service_account_key.json'

SPREADSHEET_ID = spreadsheet_id
WORKSHEET_NAME = worksheet_name

# --- Authentication and Connection ---
try:
    # Define the permissions your script needs.
    # This scope gives read/write access to Google Sheets.
    scopes = ['https://www.googleapis.com/auth/spreadsheets']

    # Load the credentials from your service account key file
    creds = Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=scopes)

    # Authorize the gspread client using these credentials
    client = gspread.authorize(creds)

    # Open the specific spreadsheet by its ID
    spreadsheet = client.open_by_key(SPREADSHEET_ID)

    # Select the specific worksheet (tab) within the spreadsheet
    worksheet = spreadsheet.worksheet(WORKSHEET_NAME)

    # --- Read Data ---
    # print(f"Successfully connected to spreadsheet ID '{SPREADSHEET_ID}' and worksheet '{WORKSHEET_NAME}'.")
    # print("\n--- Retrieving all data from the worksheet ---")
    #
    # all_data = worksheet.get_all_values()  # Get all cells as a list of lists
    #
    # if all_data:
    #     for row in all_data:
    #         print(row)
    # else:
    #     print("Worksheet is empty or no data found.")

except FileNotFoundError:
    print(f"Error: Service account key file not found at '{SERVICE_ACCOUNT_FILE}'")
    print("Please ensure the path to your 'service_account_key.json' is correct.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
    print("Please check your spreadsheet ID, worksheet name, and service account permissions.")

def connect_to_sheets(creds_path: str = "secrets/service_account_key.json") -> gspread.Worksheet:
    config = dotenv_values(".env")
    spreadsheet_id = config["SPREADSHEET_ID"]

    gc = gspread.service_account(filename=creds_path)
    return gc.open_by_key(spreadsheet_id).sheet1