#secret.py

# YouTube API Key
YOUTUBE_API_KEY = "your_youtube_API_key"

# Spotify API Credentials
SPOTIFY_CLIENT_ID = "your_spotify_client_id"
SPOTIFY_CLIENT_SECRET = "your_spotify_client_secret"
SPOTIFY_REDIRECT_URI = "http://localhost:8888/callback"
refresh_token = "AQA_t4tPObPVMv_Cf601u6k0uvl80L2Yszk8Ck22QifefJcNlC3crWkUzxDCCOBxN6h_Gj0GQbZ4wcDyk4mnjhbedBGSiaJKZ05b3AbTkU8KnfgIiFL4RBIAIz6LDP-xVgQ"  # Paste the refresh token here

# Spotify User ID
user_id = "spotify_user_id"

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
