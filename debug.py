import dropbox
import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

API_KEY = os.getenv("API_KEY_dropbox")
drpbx = dropbox.Dropbox(API_KEY)

data_folder = Path(__file__).resolve().parent / "_data"

print(f"Suche in: {data_folder}")
print(f"Gefundene CSV-Dateien: {[f.name for f in data_folder.glob('*.csv')]}")