import dropbox
import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

API_KEY = os.getenv("API_KEY_dropbox")
drpbx = dropbox.Dropbox(API_KEY)

data_folder = Path(__file__).resolve().parent / "_data"

for local_file in data_folder.glob("*.csv"):
    dropbox_file = f"/{local_file.name}"
    with open(local_file, "rb") as file:
        drpbx.files_upload(file.read(), dropbox_file, mode=dropbox.files.WriteMode("overwrite"))

for csv_file in data_folder.glob("*.csv"):
    csv_file.write_text("")