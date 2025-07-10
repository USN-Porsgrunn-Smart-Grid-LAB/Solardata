# -*- coding: utf-8 -*-

from dotenv import load_dotenv
from os import getenv
from sys import exit

load_dotenv()

# 0. Read from environment
TOKEN = getenv("SOLARLOG_TOKEN")
BASE_URL = getenv("SOLARLOG_BASE_URL")
PLANT_ID = getenv("SOLARLOG_PLANT_ID")
OUT_DIR = getenv("SOLARLOG_OUT_DIR")

import requests as req
from json import dumps

headers = { "Authorization": f"Bearer {TOKEN}"}
url = f"{BASE_URL}/visualization/plant/{PLANT_ID}/channels"

for year in [2024, 2025]:
    for month in ["01","02","03","04","05","06","07","08","09","10","11","12"]:
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
        
        print(f"Days count: {len(filtered_days)}")
        
        # 5. Write to file.
        with open(f"./{OUT_DIR}/{year}-{month}.json", "w") as out:
            out.write(dumps(filtered_days, indent=2))
