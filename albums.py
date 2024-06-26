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
def download_data(url: str) -> pd.DataFrame:
    
    results_dict = sp.playlist_tracks(url)
    tracks_data = []
    name_tracks = []
    album_names = []
    track_ids = [item["track"]["id"] for item in results_dict["items"]]
    
    # Batch call for audio features
    tracks_features = sp.audio_features(track_ids)
    
    for result, track_data in zip(results_dict["items"], tracks_features):
        track_id = result["track"]["id"]
        
        # Get track information
        track = sp.track(track_id)
        album_name = track["album"]["name"]

        name_tracks.append(result["track"]["name"])
        tracks_data.append(track_data)
        album_names.append(album_name)

    # Create a DataFrame with keys as indices and album information
    df = pd.DataFrame(tracks_data)
    df = df.assign(name=name_tracks, album=album_names)
    
    return df
def create_plot_by_album(df:pd.DataFrame,audio_feature:str)->None:
    df_grouped = df[[f"{audio_feature}", 'album']]
    # Create dot plot# Create the figure and axis
    plt.figure(figsize=(12, 8))
    ax = sns.stripplot(y=audio_feature.lower(), x='album', data=df_grouped, jitter=True, size=5, alpha=0.7, palette='Set1')

    # Customize x-tick labels (hide them) and use shorter labels or none
    ax.set_xticks([])

    # Create a legend
    handles, labels = ax.get_legend_handles_labels()
    album_labels = df['album'].unique()
    legend = plt.legend(title='Albums', labels=album_labels, loc='center left', bbox_to_anchor=(1, 0.5))

    # Customize plot
    plt.title(f'{audio_feature.capitalize()} of Songs by Album', fontsize=16)
    plt.ylabel(f'{audio_feature}', fontsize=14)
    plt.xlabel('Album', fontsize=14)

    # Show plot
    plt.show()
    # Call the function and measure time
df = download_data("https://open.spotify.com/playlist/2RuXhLrgWt5odD2RUtYItC?si=108b9c68f7204c08")
create_plot_by_album(df,"valence")