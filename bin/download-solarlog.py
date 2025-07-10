# -*- coding: utf-8 -*-

from dotenv import load_dotenv
from os import getenv, path
from sys import exit

load_dotenv()

# 0. Read from environment
TOKEN = getenv("SOLARLOG_TOKEN")
BASE_URL = getenv("SOLARLOG_BASE_URL")
PLANT_ID = getenv("SOLARLOG_PLANT_ID")
OUT_DIR = getenv("SOLARLOG_OUT_DIR")

import requests as req
from json import dumps, load

headers = { "Authorization": f"Bearer {TOKEN}"}
url = f"{BASE_URL}/visualization/plant/{PLANT_ID}/channels"

all_days = []

for year in [2024, 2025]:
    for month in ["01","02","03","04","05","06","07","08","09","10","11","12"]:
        out_file = f"./{OUT_DIR}/{year}-{month}.json"

        days = None
        if path.exists(out_file):
            print(f"{out_file} cache hit!")
            with open(out_file, "r") as file:
                days = load(file)
        else:
            # 1. Setup request
            query= f"?dateFrom={year}-{month}-01&dateTo={year}-{month}-31&channelNames%5B%5D=ProdPac"
            print(query)
            
            # 2. Do request and handle response
            res = req.get(url+query, headers=headers)
            if res.status_code != 200:
                print(f"Error: {res.status_code}")
                exit(1)

            # 3. Convert to json
            days = res.json()

        if len(days) == 0:
            continue
        
        # 4. @bugfix: There is a bug in the solarlog API, where when you ask for more days than there are in a month, you get extra days of data from the next month. It overflows to the next month.
        #    To mitigate this bug, we filter away and days which does not belong to the current month we are looking at.
        filtered_days = []
        for day in days:
            if f"{year}-{month}" in next(iter(day["dataPoints"].keys())):
                filtered_days.append(day)
                all_days.append(day)
        
        print(f"Days count: {len(filtered_days)}")
        
        # 5. Write to file.
        with open(out_file, "w") as out:
            out.write(dumps(filtered_days, indent=2))


# 6. Convert to csv...
csv_data = []
for day in all_days:
    for item in day["dataPoints"].items():
        csv_data.append(item)

csv_data = sorted(csv_data, reverse=True)
print(csv_data[0:10])
csv_data = list(filter(lambda kv: kv[1] is not None, csv_data))
timestamp,_ = csv_data[0]
datestamp = timestamp.split(":00+")[0]
csv_data = [["Timestamp", "Production[W]"]] + csv_data

import csv

with open(f"./{OUT_DIR}/solarlog-{datestamp}.csv", "w") as out:
    writer = csv.writer(out, delimiter=";")
    writer.writerows(csv_data)
