import dropbox
import os
from dotenv import load_dotenv
from pathlib import Path
import csv
from dropbox.oauth import DropboxOAuth2FlowNoRedirect
from dropbox.dropbox_client import Dropbox

load_dotenv()

APP_KEY = os.getenv("APP_KEY_dropbox")
APP_SECRET = os.getenv("APP_SECRET_dropbox")
REFRESH_TOKEN = os.getenv("REFRESH_TOKEN_dropbox")

drpbx = Dropbox(
    oauth2_refresh_token=REFRESH_TOKEN,
    app_key=APP_KEY,
    app_secret=APP_SECRET
)

data_folder = Path(__file__).resolve().parent / "_data"
current_csv = data_folder / "api_data_current.csv"

with open(current_csv, newline = "", encoding="utf-8") as f:
    reader = csv.reader(f)
    next(reader)
    first_row = next(reader)
    date_str = first_row[0].split()[0]

dropbox_folder = f"/{date_str}"

for local_file in data_folder.glob("*.csv"):
    dropbox_file = f"{dropbox_folder}/{local_file.name}"
    with open(local_file, "rb") as file:
        drpbx.files_upload(file.read(), dropbox_file, mode=dropbox.files.WriteMode("overwrite"))

for csv_file in data_folder.glob("*.csv"):
    csv_file.write_text("")