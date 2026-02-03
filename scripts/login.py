from os import getenv
from dotenv import load_dotenv
from requests import post

def login(token_url: str, client_id: str, client_secret: str):
    url = f"{token_url}/auth/realms/quotaapi/protocol/openid-connect/token"
    header = {
        "Content-type": "application/x-www-form-urlencoded"
    }
    data = { 
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret
    }

    res = post(
        url, 
        headers=header, 
        data=data
    )
    
    if res.status_code != 200:
        print(f"login Error: {res.status_code}")
        exit(1)

    return res.json()

if __name__ == "__main__":
    load_dotenv()

    CLIENT_ID = getenv("CLIENT_ID")
    CLIENT_SECRET = getenv("CLIENT_SECRET")
    TOKEN_URL = getenv("TOKEN_URL")

    token = login(TOKEN_URL, CLIENT_ID, CLIENT_SECRET)

    print(token)
