import requests as req
from dotenv import load_dotenv
import os
import csv
from pathlib import Path
from datetime import datetime
import time
import sys

load_dotenv()

API_KEY = os.getenv("API_KEY_weather")
LOCATION = "Vaterstetten"

url = f"https://api.weatherapi.com/v1/forecast.json?key={API_KEY}&q={LOCATION}&days=3"

max_retries = 3
retry_delay = 60

for attempt in range(1, max_retries + 1):
    response = req.get(url)

    if response.status_code == 200:
        try:
            data = response.json()
            break
        except ValueError:
            print(f"{datetime.now().strftime('%H:%M')} - Versuch {attempt}: Konnte JSON nicht dekodieren:", response.text)
    else:
        print(f"{datetime.now().strftime('%H:%M')} - Versuch {attempt}: Fehler vom Server: {response.status_code} - {response.text}")

    if attempt < max_retries:
        print(f"{datetime.now().strftime('%H:%M')} - Warte {retry_delay} Sekunden vor dem nächsten Versuch...")
        time.sleep(retry_delay)
    else:
        print(f"{datetime.now().strftime('%H:%M')} - Fehlgeschlagen: Alle API-Versuche sind gescheitert.")
        sys.exit(1)

current_data = data['current']
forecast_0 = data['forecast']['forecastday'][0]
forecast_1 = data['forecast']['forecastday'][1]
forecast_2 = data['forecast']['forecastday'][2]

forecasts = {
  0: forecast_0,
  1: forecast_1,
  2: forecast_2
}

entry_forecasts = {}

entry_current_data = {
  "time": current_data['last_updated'],
  "temp_c": current_data['temp_c'],
  "condition": current_data['condition']['text'],
  "wind_kph": current_data['wind_kph'],
  "wind_degree": current_data['wind_degree'],
  "wind_dir": current_data['wind_dir'],
  "precip_mm": current_data['precip_mm'],
  "humidity": current_data['humidity'],
  "cloud": current_data['cloud'],
  "feelslike_c": current_data['feelslike_c'],
  "windchill_c": current_data['windchill_c'],
  "heatindex_c": current_data['heatindex_c'],
  "vis_km": current_data['vis_km'],
  "uv": current_data['uv'],
  "gust_kph": current_data['gust_kph']
}

current_hour = datetime.now().hour

if current_data['last_updated'].endswith(":00"):
  for i in range(len(forecasts)):
    selected_forecast = forecasts[i]['hour'][current_hour]
    entry_forecasts[f"entry_forecast_{i}"] = {
      "time": selected_forecast['time'],
      "temp_c": selected_forecast['temp_c'],
      "condition": selected_forecast['condition']['text'],
      "wind_kph": selected_forecast['wind_kph'],
      "wind_degree": selected_forecast['wind_degree'],
      "wind_dir": selected_forecast['wind_dir'],
      "precip_mm": selected_forecast['precip_mm'],
      "snow_cm": selected_forecast['snow_cm'],
      "humidity": selected_forecast['humidity'],
      "cloud": selected_forecast['cloud'],
      "feelslike_c": selected_forecast['feelslike_c'],
      "windchill_c": selected_forecast['windchill_c'],
      "heatindex_c": selected_forecast['heatindex_c'],
      "will_it_rain": selected_forecast['will_it_rain'],
      "chance_of_rain": selected_forecast['chance_of_rain'],
      "will_it_snow": selected_forecast['will_it_snow'],
      "chance_of_snow": selected_forecast['chance_of_snow'],
      "vis_km": selected_forecast['vis_km'],
      "gust_kph": selected_forecast['gust_kph'],
      "uv": selected_forecast['uv']
    }

data_folder = Path(__file__).resolve().parent / "_data"

current_file = data_folder / "api_data_current.csv"

with open(current_file, "a", newline="") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=entry_current_data.keys())
    if os.stat(current_file).st_size == 0:
        writer.writeheader()
    writer.writerow(entry_current_data)


if current_data['last_updated'].endswith(":00"):
  for i in range(3):
      forecast_entry = entry_forecasts[f"entry_forecast_{i}"]
      forecast_file = data_folder / f"api_data_{i}.csv"
      with open(forecast_file, "a", newline="") as csvfile:
          writer = csv.DictWriter(csvfile, fieldnames=forecast_entry.keys())
          if os.stat(forecast_file).st_size == 0:
            writer.writeheader()
          writer.writerow(forecast_entry)