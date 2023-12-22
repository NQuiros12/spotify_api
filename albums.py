from spotipy.oauth2 import SpotifyOAuth
from spotipy import Spotify
import os
from dotenv import load_dotenv
#For getting the environment variables
load_dotenv()
song_link = "https://open.spotify.com/track/2NZUXUA8gGmXXw5MayF63k?si=bdfd71ed4c504192"

SPOTIPY_CLIENT_ID = os.getenv('SPOTIPY_CLIENT_ID')
SPOTIPY_CLIENT_SECRET =os.getenv('SPOTIPY_CLIENT_SECRET')
SPOTIPY_REDIRECT_URI = os.getenv('SPOTIPY_REDIRECT_URI')
scope = "user-library-read"

sp = Spotify(auth_manager=SpotifyOAuth(scope=scope,
                                               client_id=SPOTIPY_CLIENT_ID,
                                               client_secret=SPOTIPY_CLIENT_SECRET))

results = sp.current_user_saved_tracks()
for idx, item in enumerate(results['items']):
    track = item['track']
    print(track)
    #print(idx, track['artists'][0]['name'], " – ", track['name'])