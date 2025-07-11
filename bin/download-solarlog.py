# -*- coding: utf-8 -*-

def main():
    from dotenv import load_dotenv
    from os import getenv, path
    from sys import exit

    load_dotenv()

    # 0. Read from environment
    TOKEN = getenv("SOLARLOG_TOKEN")
    BASE_URL = getenv("SOLARLOG_BASE_URL")
    PLANT_ID = getenv("SOLARLOG_PLANT_ID")
    OUT_DIR = "./data/solarlog/"
    CACHE_DIR = "./.cache/"

    import requests as req
    import json

    headers = { "Authorization": f"Bearer {TOKEN}"}
    url = f"{BASE_URL}/visualization/plant/{PLANT_ID}/channels"

    all_days = []

    for year in [2024, 2025]:
        for month in ["01","02","03","04","05","06","07","08","09","10","11","12"]:
            cache_file = f"./{CACHE_DIR}/{year}-{month}.json"

            days = None

            if path.exists(cache_file):
                # 0. Use cache if file already exist.
                print(f"{cache_file} cache hit!")
                with open(cache_file, "r") as file:
                    days = json.load(file)
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


            # 4. @bugfix: There is a bug in the solarlog API, where when you ask for more days than there are in a month, you get extra days of data from the next month. It overflows to the next month.
            #    To mitigate this bug, we filter away and days which does not belong to the current month we are looking at.
            filtered_days = []
            for day in days:
                first_timestamp = next(iter(day["dataPoints"].keys()))
                if f"{year}-{month}" in first_timestamp:
                    filtered_days.append(day)
                    all_days.append(day)
            
            print(f"Days count: {len(filtered_days)}")
            
            # 5. Write to file.
            with open(cache_file, "w") as out:
                json_dump = json.dumps(filtered_days, indent=2)
                out.write(json_dump)


    # 6. Convert to csv...
    csv_rows = []
    for day in all_days:
        for datapoint in day["dataPoints"].items():
            if datapoint[1] is not None:
                csv_rows.append(datapoint)

    csv_rows = sorted(csv_rows, reverse=True)
    timestamp,_ = csv_rows[0]
    datestamp = timestamp.split(":00+")[0]
    csv_rows = [["Timestamp", "Production[W]"]] + csv_rows

    import csv

    with open(f"./{OUT_DIR}/solarlog-full-history-{datestamp}.csv", "w") as out:
        writer = csv.writer(out, delimiter=";")
        writer.writerows(csv_rows)


if __name__ == "__main__":
    main()