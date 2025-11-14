#secret.py

# YouTube API Key
YOUTUBE_API_KEY = "AIzaSyCRdNdCjCf1uYqvpelDK0hvQMx95MUSWCQ"

# Spotify API Credentials
SPOTIFY_CLIENT_ID = "2244f873a49a4864a27b030620f5a4cb"
SPOTIFY_CLIENT_SECRET = "08697b6a6e6f444f86f19eebae1cba17"
SPOTIFY_REDIRECT_URI = "http://localhost:8888/callback"
refresh_token = "AQA_t4tPObPVMv_Cf601u6k0uvl80L2Yszk8Ck22QifefJcNlC3crWkUzxDCCOBxN6h_Gj0GQbZ4wcDyk4mnjhbedBGSiaJKZ05b3AbTkU8KnfgIiFL4RBIAIz6LDP-xVgQ"  # Paste the refresh token here

# Spotify User ID
user_id = "31bewv5xcjwk3oqz2mpdf4znllxq"

# Base64 encoded client_id:client_secret
import base64
base_64 = base64.b64encode(f"{SPOTIFY_CLIENT_ID}:{SPOTIFY_CLIENT_SECRET}".encode()).decode()


# YouTube Playlist IDs (for video recommendations)
happy_love = "PLV5gwE4N4ej46IYyht8jXYfeIf_QzXl3_"
happy_vibes = "PLV5gwE4N4ej7tHMg2h0sCqiy9yEOIL9Zo"
sad_melancholic = "PLV5gwE4N4ej4PsACvkU9-Rp9vftyGRGci"
sad_comfort = "PLV5gwE4N4ej4gONfG4xEB7R8OIGYQI24b"
neutral_relax = "PLV5gwE4N4ej5uArPdy4Dd2VCGaLOFH02K"
neutral_focus = "PLV5gwE4N4ej66TVR8o1gcMe__RvOhdV7S"
angry_aggressive = "PLV5gwE4N4ej5WCQ0tEnjFXah7aVWL3APt"
angry_venting = "PLV5gwE4N4ej4R9S3jVdQSGDzpD6m7jDC5"
surprise_upbeat = "PLV5gwE4N4ej4WfL3KaDD6L5SqwGwk1wj-"
surprise_chill = "PLV5gwE4N4ej4cuIaC1E0341R0wIEzKC2y"
fear_calm = "PLV5gwE4N4ej578366ih1Q64JW54faXCRP"
fear_brave = "PLV5gwE4N4ej59crTMqGz-qVD4gy4DDsTB"


# Spotify Playlist IDs (for music recommendations)
mhappy_love = "1ejArTFnceNhE6RExAPw7S"
mhappy_vibes = "2YexAkphMFrm49WFlKQoKU"
msad_melancholic = "0wRf3mIXlMKjLg0TpSyq7x"
msad_comfort = "6wqLzzo1fKvzPJTLsebip1"
mneutral_relax = "7mYoC1gxOBV2NO2puldxJ3"
mneutral_focus = "2ywkYzBID3acGl8kGOWKRE"
mangry_aggressive = "7gZS5BvXexGu5zhs8yjbPV"
mangry_venting = "7iBlduYBY6xDwL3I7ErznL"
msurprise_upbeat = "6aAZeriEx2tqSk1W997wKl"
msurprise_chill = "64FOnp7wojPaoXSdUAixlU"
mfear_calm = "6sZk9Uo7Q2KbSsJRnwymdL"
mfear_brave = "49EyBWGYjifn76RTmajgtg"