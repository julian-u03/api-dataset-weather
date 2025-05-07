import dropbox
import os
from dotenv import load_dotenv
from pathlib import Path
import csv

load_dotenv()

API_KEY = os.getenv("API_KEY_dropbox")
drpbx = dropbox.Dropbox(API_KEY)

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