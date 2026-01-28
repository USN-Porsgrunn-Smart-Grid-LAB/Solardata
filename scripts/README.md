## API usage examples

The Solarlog API is documented here: https://solarlog.atlassian.net/wiki/spaces/SW/pages/8170963162/02+API.

Some extra examples are provided below, showing how to consume the Solarlog API using cURL. Hopefully this will make it easier to get started. Happy cURL-ing! 🙃


### Python and sh examples

Checkout the two examples of how to interact with the API from Python-script and shell-script respectively:
```
scripts/
  download-solarlog.py
  download-solarlog.sh
```

### Setup and run the Python-example

Make a virtual environment and install pip packages before executing the python scripts.
```sh
virtualenv .venv
source .venv/bin/activate
pip install -r scripts/requirements.txt
source .env # You have to make .env yourself. It should not be committed to Github, as it contains secrets. See .env.example for how .env should look like.
python scripts/download-solarlog.py
```

### Setup cURL

Before running any of the commands below, make sure you load the `SOLARLOG_TOKEN` and `SOLARLOG_PLANT` into your environment (see`.env.example`).


### Get Insolation, Irradiation, TempModule - /api/visualization/plant/\<plantid\>/cross-epoch/channels

**Command**
```sh
curl -H "Authorization: $SOLARLOG_TOKEN" "https://solcellespesialisten.enerest.world/api/visualization/plant/$SOLARLOG_PLANT/cross-epoch/channels?dateFrom=2025-09-02&dateTo=2025-09-02&channelNames%5B%5D=Irradiation&channelNames%5B%5D=TempModule&channelNames%5B%5D=Insolation&xComponentIds%5B%5D=594547f6-740f-4072-97e0-ec6ec6fd1c24"
```

**JSON output**
```json
[
  {
    "id": "68b618af0de159fc4688c470",
    "deviceId": "594547f6-740f-4072-97e0-ec6ec6fd1c24",
    "deviceType": "Component",
    "name": "Insolation",
    "dataPoints": {
      //...
      "2025-09-02T06:50:00+02:00": 1,
      "2025-09-02T06:55:00+02:00": 2,
      "2025-09-02T07:00:00+02:00": 2,
      "2025-09-02T07:05:00+02:00": 3,
      "2025-09-02T07:10:00+02:00": 4,
      "2025-09-02T07:15:00+02:00": 6,
      "2025-09-02T07:20:00+02:00": 8,
      "2025-09-02T07:25:00+02:00": 10,
      "2025-09-02T07:30:00+02:00": 13,
      "2025-09-02T07:35:00+02:00": 15,
      "2025-09-02T07:40:00+02:00": 19,
      "2025-09-02T07:45:00+02:00": 22,
      "2025-09-02T07:50:00+02:00": 27,
      //...
    },
    "date": "2025-09-02",
    "unit": "Wh/m²"
  },
  {
    "id": "68b618af0de159fc4688c46c",
    "deviceId": "594547f6-740f-4072-97e0-ec6ec6fd1c24",
    "deviceType": "Component",
    "name": "Irradiation",
    "dataPoints": {
      //...
      "2025-09-02T06:50:00+02:00": 5,
      "2025-09-02T06:55:00+02:00": 7,
      "2025-09-02T07:00:00+02:00": 8,
      "2025-09-02T07:05:00+02:00": 11,
      "2025-09-02T07:10:00+02:00": 14,
      "2025-09-02T07:15:00+02:00": 19,
      "2025-09-02T07:20:00+02:00": 23,
      "2025-09-02T07:25:00+02:00": 26,
      "2025-09-02T07:30:00+02:00": 29,
      "2025-09-02T07:35:00+02:00": 35,
      "2025-09-02T07:40:00+02:00": 37,
      "2025-09-02T07:45:00+02:00": 46,
      "2025-09-02T07:50:00+02:00": 53,
      //...
    },
    "date": "2025-09-02",
    "unit": "W/m²"
  },
  {
    "id": "68b618af0de159fc4688c46d",
    "deviceId": "594547f6-740f-4072-97e0-ec6ec6fd1c24",
    "deviceType": "Component",
    "name": "TempModule",
    "dataPoints": {
      //...
      "2025-09-02T06:50:00+02:00": 15,
      "2025-09-02T06:55:00+02:00": 15,
      "2025-09-02T07:00:00+02:00": 15,
      "2025-09-02T07:05:00+02:00": 15,
      "2025-09-02T07:10:00+02:00": 15,
      "2025-09-02T07:15:00+02:00": 15,
      "2025-09-02T07:20:00+02:00": 15,
      "2025-09-02T07:25:00+02:00": 14,
      "2025-09-02T07:30:00+02:00": 14,
      "2025-09-02T07:35:00+02:00": 14,
      "2025-09-02T07:40:00+02:00": 14,
      "2025-09-02T07:45:00+02:00": 14,
      "2025-09-02T07:50:00+02:00": 14,
      //...
    },
    "date": "2025-09-02",
    "unit": "°C"
  }
]
```

###  Get plant info - /api/visualization/plant/\<plantid\>

```sh
curl -H "Authorization: $SOLARLOG_TOKEN" "https://solcellespesialisten.enerest.world/api/visualization/plant/$SOLARLOG_PLANT"

```
```json
{
    "id":"1ef59795-736c-625a-9362-6b06f3426853",
    "label":"USN Porsgrunn",
    "vendor":"SDS",
    "fleets":[{"id":"36bfebf1-bae6-11ea-bcf6-001e6799788c"}],
    "healthStatus":"OK",
    "deviceFullName":"Solar-Log Base 100",
    "targetPercentage":null,
    "migrationInProgress":false,
    "size":44000,
    "componentsClasses":["production","sensors","consumption","meter","hidden","intern"]
}
```


### Get plant components - /api/datasource/plant/\<plantid\>/components
```sh
curl -H "Authorization: $SOLARLOG_TOKEN" "https://solcellespesialisten.enerest.world/api/datasource/plant/$SOLARLOG_PLANT/components?properties[]=classes&properties[]=dataindex&properties[]=id&properties[]=moduleField&properties[]=moduleStrings&properties[]=mpptrackers&properties[]=name&properties[]=sortOrder&properties[]=type&properties[]=visualizationChannels&properties[]=crossEpochId&properties[]=epochActiveFrom&from=2025-9-2&to=2025-9-2"
```
```json
[
    {
        "id": "d4e33492-69f3-11ef-b415-ffbedf4d5a30",
        "mpptrackers": [
            {
                "id": "d4e33820-69f3-11ef-badf-ffbedf4d5a30",
                "moduleString": null,
                "moduleStrings": [],
                "trackerindex": 1,
                "moduleField": {
                    "id": "d4e33988-69f3-11ef-91a2-ffbedf4d5a30",
                    "label": "1",
                    "index": 1,
                    "orientation": null,
                    "tilt": null,
                    "monitored": true
                },
                "size": 10000,
                "name": "MPPT 1",
                "visualizationChannels": [
                    "ProdPdc",
                    "ProdPdcNorm",
                    "ProdUdc",
                    "ProdIdc"
                ]
            },
            {
                "id": "d4e33a50-69f3-11ef-8f7c-ffbedf4d5a30",
                "moduleString": null,
                "moduleStrings": [],
                "trackerindex": 2,
                "moduleField": {
                    "id":"d4e33988-69f3-11ef-91a2-ffbedf4d5a30",
                    "label":"1",
                    "index":1,"orientation":null,"tilt":null,"monitored":true
                },
                "size":10000,
                "name":"MPPT 2",
                "visualizationChannels":["ProdPdc","ProdPdcNorm","ProdUdc","ProdIdc"]
            },
            {
                "id":"d4e33b04-69f3-11ef-94aa-ffbedf4d5a30",
                "moduleString":null,
                "moduleStrings":[],
                "trackerindex":3,
                "moduleField":{"id":"d4e33988-69f3-11ef-91a2-ffbedf4d5a30","label":"1","index":1,"orientation":null,"tilt":null,"monitored":true},
                "size":10000,
                "name":"MPPT 3",
                "visualizationChannels":["ProdPdc","ProdPdcNorm","ProdUdc","ProdIdc"]
            },
            ...
]}]
```
