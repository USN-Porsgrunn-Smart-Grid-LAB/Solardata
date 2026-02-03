## API usage examples

The Solarlog API is documented here: https://solarlog.atlassian.net/wiki/spaces/SWN/pages/267740250126/02+API

### Postman

A Postman collection and environment can be found in ../postman. The only thing missing in the environment is the client secret. Add it to get started. Client secret can be found in the portal [here](https://solcellespesialisten.enerest.world/user-settings/api/user-overview/9682c025-f25e-4d7e-9358-925abef1923c).

### Python

Checkout the examples of how to interact with the API from Python-script:
```
scripts/
  download-solarlog.py
```

### Setup and run the Python-example

Make a virtual environment and install pip packages before executing the python scripts.
```sh
virtualenv .venv
source .venv/bin/activate
pip install -r scripts/requirements.txt
cp scripts/.env.example .env 
source .env   # Add client-secret to .env.
python scripts/download-solarlog.py
```
