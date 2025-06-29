import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

def connect_to_sheet(sheet_name):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name('creds.json', scope)
    client = gspread.authorize(creds)
    return client.open(sheet_name)

def log_trades(df, sheet):
    worksheet = sheet.worksheet("Trade_Log")
    worksheet.update([df.columns.values.tolist()] + df.values.tolist())

def log_summary(stats, sheet):
    worksheet = sheet.worksheet("Summary")
    worksheet.update('A1', [[k, v] for k, v in stats.items()]) 