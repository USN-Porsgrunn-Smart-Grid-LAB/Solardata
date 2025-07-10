#!/bin/sh

. ./.env # <-- Put SOLARLOG_TOKEN=<TOKEN> in this file

for year in 2024 2025; do
    for month in 01 02 03 04 05 06 07 08 09 10 11 12; do
        echo "$year-$month..."
        curl -H "Authorization: Bearer $SOLARLOG_TOKEN" \
            "$SOLARLOG_BASE_URL/visualization/plant/$SOLARLOG_PLANT_ID/channels?dateFrom=$year-$month-01&dateTo=$year-$month-31&channelNames%5B%5D=ProdPac" \
            | jq \
            > ./$SOLARLOG_OUT_DIR/$year-$month.json
    done
    echo "$year done!"
done
echo "Done!"