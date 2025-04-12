import os
import requests
import json

# Get Spotidy Client ID and secret
clientId = os.environ.get('CLIENT_ID')
clientSecret = os.environ.get('CLIENT_SECRET')

# Get Auth Token
grant_type = 'client_credentials'
body_params = {'grant_type' : grant_type}

url="https://accounts.spotify.com/api/token"
response = requests.post(url, data=body_params, auth = (clientId, clientSecret)) 

token_raw = json.loads(response.text)
token = token_raw["access_token"]
print(token)