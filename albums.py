from spotipy.oauth2 import SpotifyOAuth
from spotipy import Spotify
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
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
results_dict = sp.playlist_tracks("https://open.spotify.com/playlist/2RuXhLrgWt5odD2RUtYItC?si=108b9c68f7204c08")
tracks_data = []
name_tracks = []
for result in results_dict["items"]:
    track_data = sp.audio_features(result["track"]["id"])[0]  # Get audio features for each track
    name_tracks.append(result["track"]["name"])
    tracks_data.append(track_data)

# Create a DataFrame with keys as indices
df = pd.DataFrame(tracks_data)
df = df.assign(name=name_tracks)