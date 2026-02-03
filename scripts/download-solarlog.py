# -*- coding: utf-8 -*-
from os import getenv, path, makedirs, path
from sys import exit
import json
import csv
from dotenv import load_dotenv
import requests as req

from login import login

def main():
    load_dotenv()

    # 0. Read config from environment
    CLIENT_ID = getenv("CLIENT_ID")
    CLIENT_SECRET = getenv("CLIENT_SECRET")
    TOKEN_URL = getenv("TOKEN_URL")
    SOLARLOG_SENSOR = getenv("SOLARLOG_SENSOR")
    OUT_DIR = "./data/solarlog"


    # 1. Login
    res = login(TOKEN_URL, CLIENT_ID, CLIENT_SECRET)

    # 2. Collect data from all the channels
    data = {}

    channel = get_channel(channel="ProdPac", token=res["access_token"])
    append_to_data(data, channel)

    channel = get_channel(sensor=SOLARLOG_SENSOR, channel="Irradiation", token=res["access_token"])
    append_to_data(data, channel)

    channel = get_channel(sensor=SOLARLOG_SENSOR, channel="TempModule", token=res["access_token"])
    append_to_data(data, channel)
    
    channel = get_channel(sensor=SOLARLOG_SENSOR, channel="TempAmbient", token=res["access_token"])
    append_to_data(data, channel)

    channel = get_channel(sensor=SOLARLOG_SENSOR, channel="WindVelocity", token=res["access_token"])
    append_to_data(data, channel)


    # 3. Convert .json to .csv...
    csv_rows = []
    for key, values in data.items():
        csv_rows.append([key, *values])

    timestamp, *rest = csv_rows[0]
    datestamp = (timestamp.split(":00+")[0]).replace(":", "_")
    csv_rows = [[
        "Timestamp", 
        "Production[W]", 
        "Irradiation[W/m2]", 
        "TempModule[°C]", 
        "TempAmbient[°C]",
        "WindVelocity[m/s]"
        ]] + csv_rows

    with open(f"{OUT_DIR}/solarlog-full-history-{datestamp}.csv", "w") as out:
        writer = csv.writer(out, delimiter=";")
        writer.writerows(csv_rows)


def append_to_data(data, days):
    for day in days:
        for timestamp, value in day["dataPoints"].items():
            if value is not None:
                if timestamp in data:
                    data[timestamp].append(value)
                else:
                    data[timestamp] = [value]

def get_channel(token: str, channel: str, sensor: str | None = None):

    # 0. Read config from environment
    BASE_URL = getenv("SOLARLOG_BASE_URL")
    PLANT_ID = getenv("SOLARLOG_PLANT")
    DATE_FROM = getenv("DATE_FROM")
    DATE_TO = getenv("DATE_TO")
    CACHE_DIR = "./.cache"

    # 2. Setup request
    QUERY = f"\
dateFrom={DATE_FROM}&\
dateTo={DATE_TO}&\
channelNames[]={channel}"

    if sensor:
        QUERY += f"&componentIds[]={sensor}"

    URL = f"{BASE_URL}/visualization/plant/{PLANT_ID}/channels?{QUERY}"
    headers = { "Authorization": f"Bearer {token}"}

    # 3. Setup cache
    cache_file = f"{CACHE_DIR}/{channel}.json"
    days = None

    if path.exists(cache_file):
        # 4a Use cache if already exist
        print(f"{cache_file} cache hit!")
        with open(cache_file, "r") as file:
            days = json.load(file)
    else:
        # 4b. Do request if cache does not exist
        res = req.get(URL, headers=headers)
        print(res.url)            
        if res.status_code != 200:
            print(f"[{channel}] Error: {res.status_code}")
            print(f"[{channel}] Header", res.headers)
            print(f"[{channel}] Text", res.text)
            exit(1)

        days = res.json()

        # 5. Write to file.
        makedirs(path.dirname(cache_file), exist_ok=True)
        with open(cache_file, "w") as out:
            json_dump = json.dumps(days, indent=2)
            out.write(json_dump)

    return days

if __name__ == "__main__":
    main()