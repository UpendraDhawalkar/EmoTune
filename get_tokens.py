import requests
import base64

# Spotify API credentials
CLIENT_ID = ""  # Replace with your Spotify Client ID
CLIENT_SECRET = ""  # Replace with your Spotify Client Secret
REDIRECT_URI = "http://localhost:8888/callback"  # Must match the redirect URI in your Spotify app
AUTHORIZATION_CODE = "AQBRsCI8Gu0jISBBIUdRsTOwj96aJkm7C0KQy8wk7NAnFq3O0jnJGie5w-6Gfbwm1W7UxRyq6TlRhPSzuWe_Cker2Kj_P2wzd441FMsm8YjXZ_eu42Yvha81mqrTmj3hHTTt176mrsE_3kn1HqDQb2ZGq0rz3zThBNQMbOkl_fHRdPaBwPirom2Xe-gCS-nLVtnCJmP5DxaeodTvY71F8VGVqnT77A"  # Replace with the code you got from the callback

# Base64 encode client_id:client_secret
credentials = f"{CLIENT_ID}:{CLIENT_SECRET}"
base64_credentials = base64.b64encode(credentials.encode()).decode()

# Request tokens
url = "https://accounts.spotify.com/api/token"
headers = {
    "Authorization": f"Basic {base64_credentials}",
    "Content-Type": "application/x-www-form-urlencoded"
}
data = {
    "grant_type": "authorization_code",
    "code": AUTHORIZATION_CODE,
    "redirect_uri": REDIRECT_URI
}

# Make the request
response = requests.post(url, headers=headers, data=data)
if response.status_code == 200:
    tokens = response.json()
    access_token = tokens["access_token"]
    refresh_token = tokens["refresh_token"]
    print("Access Token:", access_token)
    print("Refresh Token:", refresh_token)
else:
    print("Error:", response.status_code, response.text)
