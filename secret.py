#secret.py

# YouTube API Key
YOUTUBE_API_KEY = ""

# Spotify API Credentials
SPOTIFY_CLIENT_ID = ""
SPOTIFY_CLIENT_SECRET = ""
SPOTIFY_REDIRECT_URI = "http://localhost:8888/callback"
refresh_token = ""  # Paste the refresh token here

# Spotify User ID
user_id = ""

# Base64 encoded client_id:client_secret
import base64
base_64 = base64.b64encode(f"{SPOTIFY_CLIENT_ID}:{SPOTIFY_CLIENT_SECRET}".encode()).decode()


# YouTube Playlist IDs (for video recommendations)
happy_love = ""
happy_vibes = ""
sad_melancholic = ""
sad_comfort = ""
neutral_relax = ""
neutral_focus = ""
angry_aggressive = ""
angry_venting = ""
surprise_upbeat = ""
surprise_chill = ""
fear_calm = ""
fear_brave = ""


# Spotify Playlist IDs (for music recommendations)
mhappy_love = ""
mhappy_vibes = ""
msad_melancholic = ""
msad_comfort = ""
mneutral_relax = ""
mneutral_focus = ""
mangry_aggressive = ""
mangry_venting = ""
msurprise_upbeat = ""
msurprise_chill = ""
mfear_calm = ""
mfear_brave = ""