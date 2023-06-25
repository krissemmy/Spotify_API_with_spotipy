"""
pip install dotenv, spotipy
create a .env file which will contain your Client_id and Client_secret in a string format
"""

import os
import spotipy
from dotenv import load_dotenv
import pandas as pd
from spotipy.oauth2 import SpotifyOAuth



class Spotify:
    load_dotenv()

    def __init__(self):
        self.Client_Id = os.getenv("CLIENT_ID") # Retrieves the Client ID from the .env file
        self.Client_Secret = os.getenv("CLIENT_SECRET") # Retrieves the Client Secret from the .env file
        self.redirect_uri = "http://localhost:8888/callback"

    def get_all_songs(self):
        """
        Retrieves all the songs saved in the user's Spotify library and writes them to a CSV file.
        """

        scope1 = "user-library-read" 

        result = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope1, client_id=self.Client_Id, client_secret=self.Client_Secret, redirect_uri=self.redirect_uri))
        r = result.current_user_saved_tracks()
        
        count = round(r['total']/20)
        id = 0

        for i in range(count):
            r = result.current_user_saved_tracks(offset=id)
            for i in r['items']:
                with open('spotify_data.csv','a',newline='') as file:
                    track_u = i['track']['uri']
                    reel = result.track(track_id=track_u)
                    reel_name = reel['name']
                    x = [v['name'] for v in reel['artists']]
                    file.write(f"{reel_name} | {x} | {track_u}\n")
            id += 20

        
    def del_duplicate_tracks(Client_Id, Client_Secret):
        """
        Deletes duplicate tracks from the user's Spotify library based on the song URI.

        Parameters:
        Client_Id (str): Spotify Client ID.
        Client_Secret (str): Spotify Client Secret.
        """

        Client_Id = self.Client_Id
        Client_Secret = self.Client_Secret
        Redirect_URL = self.redirect_uri

        df = pd.read_csv("spotify_data.csv", header=None, delimiter="|")
        df.columns=["song_name","artists","song_uri"]
        duplicate_song_uri = df[df["song_name"].duplicated()]["song_uri"]
        duplicate_list = list(duplicate_song_uri.values)
        new_duplicate_list = [i.split(':')[2] for i in duplicate_list]

        scope2 = "user-library-modify"

        real = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope2,client_id=Client_Id, client_secret=Client_Secret, redirect_uri=Redirect_URL))
        for i in new_duplicate_list:
            real.current_user_saved_tracks_delete(tracks=i)
        
    def get_top_tracks(self):
        """
        Retrieves the user's top tracks from Spotify for different time ranges and writes them to separate CSV files.
        """

        # Set the necessary variables
        Redirect_URL = self.redirect_uri
        Client_Id = self.Client_Id
        Client_Secret = self.Client_Secret
        scope3 = "user-top-read"

        # Create a Spotify object for API access and authentication
        spoti = spotipy.Spotify(auth_manager=SpotifyOAuth(scope= scope3, client_id = client_id, client_secret= client_secret, redirect_uri= redirect_uri))
        
        # Initialize counters and retrieve the top tracks
        top = spoti.current_user_top_tracks()
        id = 0

        for i in range(5):
            rank = 1
            # Retrieve and process the user's top tracks for the short-term time range
            top_track_daily = spoti.current_user_top_tracks(offset= id, time_range='short_term')
            for i in top_track_daily['items']:
                with open('top_track_daily.csv','a',newline='') as file:
                    file.write(f"{rank} | {i['artists'][0]['name']} | {i['name']}\n")
                rank += 1
            
            # Retrieve and process the user's top tracks for the weekly time range
            top_track_weekly = spoti.current_user_top_tracks(offset=id)
            rank1 = 1
            for i in top_track_weekly['items']:
                with open('top_track_weekly.csv','a',newline='') as file:
                    file.write(f"{rank1} | {i['artists'][0]['name']} | {i['name']}\n")
                rank1 += 1
            
            # Retrieve and process the user's top tracks for the long-term time range
            top_track_long_term = spoti.current_user_top_tracks(offset= id, time_range='long_term')
            rank2 = 1
            for i in top_track_long_term['items']:
                with open('top_track_long_term.csv','a',newline='') as file:
                    file.write(f"{rank2} | {i['artists'][0]['name']} | {i['name']}\n")
                rank2 += 1

            id += 20
        

        # Read the CSV files and display the top tracks for each time range
        df1 = pd.read_csv("top_track_daily.csv", header=None, delimiter="|")
        df1.columns=["rank", "artist_name", "track_name"]
        print(df1.head(),"\n")

        df2 = pd.read_csv("top_track_weekly.csv", header=None, delimiter="|")
        df2.columns=["rank", "artist_name", "track_name"]
        print(df2.head(),"\n")

        df3 = pd.read_csv("top_track_long_term.csv", header=None, delimiter="|")
        df3.columns=["rank", "artist_name", "track_name"]
        print(df3.head())



spotify = Spotify()
