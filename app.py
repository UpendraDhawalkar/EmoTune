# app.py
import os
import json
import cv2
import requests
import numpy as np
from flask import Flask, render_template, request, Response, session, jsonify, redirect, url_for
from google_auth_oauthlib.flow import Flow
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from keras.models import load_model
from keras.preprocessing.image import img_to_array
import time
import secret
from refresh import Refresh  

# Initialize Flask app
app = Flask(__name__)
app.secret_key = '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'  # Change this to a secure random key

# Configuration
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'  # Remove in production
CLIENT_SECRETS_FILE = "client_secrets.json"
SCOPES = ['openid', 'https://www.googleapis.com/auth/userinfo.profile', 
          'https://www.googleapis.com/auth/userinfo.email']
REDIRECT_URI = 'http://localhost:5000/callback'

# Emotion Detection Setup
face_classifier = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
classifier = load_model('fer.h5')
emotion_labels = ['Angry', 'Fear', 'Happy', 'Neutral', 'Sad', 'Surprise']

# Session Configuration
app.config.update(
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE='Lax'
)

@app.route('/')
def main():
    return render_template('main.html')

@app.route('/check-login')
def check_login():
    return jsonify({'loggedIn': 'credentials' in session})

@app.route('/login')
def login():
    # Create new flow instance for each login attempt
    flow = Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE,
        scopes=SCOPES,
        redirect_uri=REDIRECT_URI
    )
    
    authorization_url, state = flow.authorization_url(
        access_type='offline',
        prompt='consent',
        include_granted_scopes='true'
    )
    
    # Store the state and flow details in session
    session['oauth_flow'] = {
        'state': state,
        'redirect_uri': REDIRECT_URI
    }
    
    return redirect(authorization_url)

@app.route('/callback')
def callback():
    # Retrieve stored flow data
    flow_data = session.get('oauth_flow', {})
    stored_state = flow_data.get('state')
    received_state = request.args.get('state')
    
    # Validate state parameter
    if not stored_state or stored_state != received_state:
        return render_template('main.html',
                            error_message="Invalid state parameter - possible security issue",
                            details=f"Stored: {stored_state}\nReceived: {received_state}"), 400
    
    try:
        # Recreate the flow instance
        flow = Flow.from_client_secrets_file(
            CLIENT_SECRETS_FILE,
            scopes=SCOPES,
            state=stored_state,
            redirect_uri=flow_data['redirect_uri']
        )
        
        # Exchange authorization code for tokens
        flow.fetch_token(authorization_response=request.url)
        credentials = flow.credentials
        
        # Store credentials in session
        session['credentials'] = {
            'token': credentials.token,
            'refresh_token': credentials.refresh_token,
            'token_uri': credentials.token_uri,
            'client_id': credentials.client_id,
            'client_secret': credentials.client_secret,
            'scopes': credentials.scopes
        }
        
        # Get user info
        userinfo_service = build('oauth2', 'v2', credentials=credentials)
        user_info = userinfo_service.userinfo().get().execute()
        
        session['user'] = {
            'name': user_info.get('name'),
            'email': user_info.get('email'),
            'picture': user_info.get('picture')
        }
        
        # Clear the temporary flow data
        session.pop('oauth_flow', None)
        
        return redirect(url_for('main'))
    
    except Exception as e:
        return render_template('main.html',
                            error_message="Authentication failed",
                            details=str(e)), 400

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('main'))


def generate_frames():
    camera = cv2.VideoCapture(0)
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            capture_duration = 5
            start_time = time.time()
            while(int(time.time() - start_time) < capture_duration):
                _, frame = camera.read()
                frame = cv2.flip(frame, 1)
                labels = []
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = face_classifier.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5, 
                                                       minSize=(30, 30), flags=cv2.CASCADE_SCALE_IMAGE)

                for (x, y, w, h) in faces:
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 255), 2)
                    roi_gray = gray[y:y+h, x:x+w]
                    roi_gray = cv2.resize(roi_gray, (48, 48), interpolation=cv2.INTER_AREA)

                    if np.sum([roi_gray]) != 0:
                        roi = roi_gray.astype('float')/255.0
                        roi = img_to_array(roi)
                        roi = np.expand_dims(roi, axis=0)
                        prediction = classifier.predict(roi)[0]
                        global label
                        label = emotion_labels[prediction.argmax()]
                        label_position = (x, y)
                        cv2.putText(frame, label, label_position, 
                                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                ret, buffer = cv2.imencode('.jpg', frame)
                frame = buffer.tobytes()
                cv2.waitKey(0)
                yield(b'--frame\r\n'
                      b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/index')
def index():
    if 'credentials' not in session:
        return redirect(url_for('login'))
    session.pop('detected_mood', None)  # Clear previous mood
    return render_template('index.html', user=session.get('user'))

@app.route('/video')
def video():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/get-recommended-videos')
def get_recommended_videos():
    if 'credentials' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    try:
        mood_playlists = {
            'happy': secret.happy_love,
            'sad': secret.sad_comfort,
            'neutral': secret.neutral_focus,
            'angry': secret.angry_aggressive,
            'surprise': secret.surprise_chill,
            'fear': secret.fear_brave
        }
        
        youtube = build('youtube', 'v3', developerKey=secret.YOUTUBE_API_KEY)
        
        all_videos = []
        for mood, playlist_id in mood_playlists.items():
            try:
                request = youtube.playlistItems().list(
                    part="snippet",
                    playlistId=playlist_id,
                    maxResults=3  # Get at least 3 videos per mood
                )
                response = request.execute()
                
                for item in response.get('items', []):
                    snippet = item.get('snippet', {})
                    video_id = snippet.get('resourceId', {}).get('videoId')
                    thumbnails = snippet.get('thumbnails', {})
                    
                    if video_id:
                        all_videos.append({
                            'id': video_id,
                            'title': snippet.get('title', 'Unknown Video'),
                            'thumbnail': thumbnails.get('high', {}).get('url', ''),
                            'duration': '10:30',  # You can get duration from videoDetails if needed
                            'views': '1.2M',      # You can get viewCount from videoDetails if needed
                            'mood': mood
                        })
            except Exception as e:
                print(f"Error fetching videos for mood {mood}: {str(e)}")
                continue
        
        # If we didn't get enough videos from some moods, try to compensate
        if len(all_videos) < 12:  # At least 2 per mood * 6 moods
            # Try to get more videos from moods that have them
            for mood, playlist_id in mood_playlists.items():
                if len([v for v in all_videos if v['mood'] == mood]) < 2:
                    try:
                        request = youtube.playlistItems().list(
                            part="snippet",
                            playlistId=playlist_id,
                            maxResults=5  # Get more videos for this mood
                        )
                        response = request.execute()
                        
                        for item in response.get('items', []):
                            snippet = item.get('snippet', {})
                            video_id = snippet.get('resourceId', {}).get('videoId')
                            thumbnails = snippet.get('thumbnails', {})
                            
                            if video_id and len([v for v in all_videos if v['mood'] == mood]) < 2:
                                all_videos.append({
                                    'id': video_id,
                                    'title': snippet.get('title', 'Unknown Video'),
                                    'thumbnail': thumbnails.get('high', {}).get('url', ''),
                                    'duration': '10:30',
                                    'views': '1.2M',
                                    'mood': mood
                                })
                    except Exception as e:
                        print(f"Error fetching additional videos for mood {mood}: {str(e)}")
                        continue
        
        return jsonify({'videos': all_videos})
        
    except Exception as e:
        print(f"Video recommendation error: {str(e)}")
        return jsonify({'error': str(e)}), 500
    
@app.route('/video-details')
def video_details():
    video_id = request.args.get('id')
    if not video_id:
        return jsonify({'error': 'Video ID required'}), 400
    
    try:
        # Fetch video details from YouTube API
        url = 'https://www.googleapis.com/youtube/v3/videos'
        params = {
            'key': secret.YOUTUBE_API_KEY,
            'id': video_id,
            'part': 'snippet,statistics,contentDetails'
        }
        
        response = requests.get(url, params=params)
        if response.status_code != 200:
            return jsonify({'error': 'YouTube API request failed'}), 500
            
        return jsonify(response.json())
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/get-mood-mix')
def get_mood_mix():
    if 'credentials' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    try:
        mood_playlists = {
            'happy': secret.mhappy_love,
            'sad': secret.msad_comfort,
            'neutral': secret.mneutral_focus,
            'angry': secret.mangry_aggressive,
            'surprise': secret.msurprise_chill,
            'fear': secret.mfear_brave
        }
        
        refreshCaller = Refresh()
        spotify_token = refreshCaller.refresh()
        
        all_tracks = []
        for mood, playlist_id in mood_playlists.items():
            response = requests.get(
                f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks",
                headers={
                    "Authorization": f"Bearer {spotify_token}",
                    "Content-Type": "application/json"
                },
                params={
                    'fields': 'items(track(id,name,artists(name),uri))',
                    'limit': 5  # Get 5 tracks per mood
                }
            )
            
            if response.status_code == 200:
                for item in response.json().get('items', []):
                    track = item.get('track')
                    if track:
                        all_tracks.append({
                            'id': track.get('id'),
                            'name': track.get('name', 'Unknown Track'),
                            'artist': ', '.join([a['name'] for a in track.get('artists', [])]),
                            'uri': track.get('uri'),
                            'mood': mood
                        })
        
        # Shuffle the tracks for variety
        import random
        random.shuffle(all_tracks)
        
        return jsonify({'tracks': all_tracks[:15]})  # Return first 15 shuffled tracks
        
    except Exception as e:
        print(f"Mood mix error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/result', methods=["POST", "GET"])
def playlistmanager():
    if 'credentials' not in session:
        return redirect(url_for('login'))
    
    # Get mood from session or global label
    input = session.get('detected_mood')
    if not input:
        try:
            input = label
            session['detected_mood'] = input  # Store in session
        except NameError:
            return Response("Emotion was not detected properly")
    
    # Handle both GET and POST requests safely
    if request.method == 'POST':
        option = request.form.get('btnradio')
    else:
        option = request.args.get('btnradio')
    
    if not option:
        return Response("No option selected"), 400
    
    sub_option = request.values.get('sub_option', 'default')
    print(f"option is {option}, sub_option is {sub_option}, mood is {input}")

        # Playlist selection - updated nested structure
    playlist_map = {
            'Happy': {
                'music': {'love': secret.mhappy_love, 'vibes': secret.mhappy_vibes},
                'video': {'love': secret.happy_love, 'vibes': secret.happy_vibes}
            },
            'Sad': {
                'music': {'melancholic': secret.msad_melancholic, 'comfort': secret.msad_comfort},
                'video': {'melancholic': secret.sad_melancholic, 'comfort': secret.sad_comfort}
            },
            'Neutral': {
                'music': {'relax': secret.mneutral_relax, 'focus': secret.mneutral_focus},
                'video': {'relax': secret.neutral_relax, 'focus': secret.neutral_focus}
            },
            'Angry': {
                'music': {'aggressive': secret.mangry_aggressive, 'venting': secret.mangry_venting},
                'video': {'aggressive': secret.angry_aggressive, 'venting': secret.angry_venting}
            },
            'Surprise': {
                'music': {'upbeat': secret.msurprise_upbeat, 'chill': secret.msurprise_chill},
                'video': {'upbeat': secret.surprise_upbeat, 'chill': secret.surprise_chill}
            },
            'Fear': {
                'music': {'calm': secret.mfear_calm, 'brave': secret.mfear_brave},
                'video': {'calm': secret.fear_calm, 'brave': secret.fear_brave}
            }
        }

        # Get the correct playlist ID from nested structure
    try:
            playlist_id = playlist_map[input][option][sub_option]
    except KeyError:
            # Fallback to first available sub-option if specified one doesn't exist
            try:
                first_sub = next(iter(playlist_map[input][option].values()))
                playlist_id = first_sub
                sub_option = next(iter(playlist_map[input][option].keys()))  # Update sub_option to match
            except (KeyError, StopIteration):
                return Response("Invalid emotion or option selected")

    if option == "video":
            search_url = 'https://www.googleapis.com/youtube/v3/playlistItems'
            search_params = {
                'key': secret.YOUTUBE_API_KEY,
                'playlistId': playlist_id,
                'part': 'contentDetails',
                'maxResults': 50 
            }

            r = requests.get(search_url, params=search_params)
            if r.status_code != 200:
                return Response(f"YouTube API error: {r.status_code} - {r.text}")

            try:
                video_ids = [item['contentDetails']['videoId'] for item in r.json()['items']]
                return render_template('results.html', 
                                    input=input, 
                                    video_ids=video_ids, 
                                    user=session.get('user'),
                                    current_sub_option=sub_option)  # Pass sub-option to template
            except KeyError as e:
                return Response(f"Error processing YouTube response: {str(e)}")

    else:
            print("Refreshing Spotify token...")
            try:
                refreshCaller = Refresh()
                spotify_token = refreshCaller.refresh()
                
                query = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
                params = {
                    'fields': 'items(track(id,name,artists(name),duration_ms,popularity))',
                    'limit': 50
                }
                
                headers = {
                    "Authorization": f"Bearer {spotify_token}",
                    "Content-Type": "application/json"
                }

                response = requests.get(query, headers=headers, params=params)
                if response.status_code != 200:
                    return Response(f"Spotify API error: {response.status_code} - {response.text}")

                tracks = []
                for item in response.json().get('items', []):
                    track = item.get('track')
                    if track:
                        tracks.append({
                            'id': track.get('id'),
                            'name': track.get('name', 'Unknown Track'),
                            'artist': ', '.join([a['name'] for a in track.get('artists', [])]),
                            'duration_ms': track.get('duration_ms', 0),
                            'popularity': track.get('popularity', 0),
                            'duration_formatted': format_duration(track.get('duration_ms', 0))
                        })

                tracks.sort(key=lambda x: x['name'].lower())
                
                return render_template('music.html', 
                     input=input, 
                     tracks=tracks,
                     user=session.get('user'),
                     current_sub_option=sub_option)  # Make sure this is passed # Pass sub-option to template

            except Exception as e:
                print(f"Spotify error: {str(e)}")
                return Response(f"Error processing Spotify data: {str(e)}")

def format_duration(ms):
    """Convert milliseconds to minutes:seconds format"""
    seconds = int((ms / 1000) % 60)
    minutes = int((ms / (1000 * 60)) % 60)
    return f"{minutes}:{seconds:02d}"

if __name__ == '__main__':
    app.run(debug=True)
    