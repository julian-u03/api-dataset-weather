from pathlib import Path

data_folder = Path(__file__).resolve().parent / "_data"

for csv_file in data_folder.glob("*.csv"):
    csv_file.write_text("")