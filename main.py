import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os
import spotipy

load_dotenv('/Users/natha/PycharmProjects/info.env')

client_id = os.getenv('SPOTIFY_CLIENT_ID')
client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')

input_date = input('type a date in yyyy/mm/dd format:')
date = input_date.split('/')
link = f'https://www.billboard.com/charts/hot-100/{date[0]}-{date[1]}-{date[2]}/'
html_file = requests.get(link).text
soup = BeautifulSoup(html_file, 'html.parser')
scraped_songs = soup.select('li h3')
songs = [song.text.strip() for song in scraped_songs[:100]]

auth = spotipy.SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri='http://example.com',
                            scope='playlist-modify-private', cache_path='token.txt', show_dialog=True)
sp = spotipy.Spotify(auth_manager=auth)
user_id = sp.current_user()["id"]

playlist_id = sp.user_playlist_create(user_id, input_date, False, False, "your_description")['id']

song_uris = []
for song in songs:
    track = f'track: {song} year: {date[0]}'
    result = sp.search(q=track)
    try:
        song_uris.append(result['tracks']['items'][0]['uri'])
    except IndexError:
        print("Didn't work")
sp.playlist_add_items(playlist_id, song_uris)
