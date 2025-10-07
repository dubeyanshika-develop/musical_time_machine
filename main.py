import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import requests
from bs4 import BeautifulSoup


SPOTIFY_TOKEN_ENDPOINT = 'https://accounts.spotify.com/api/token'
BILLBOARD_BASE_URL="https://www.billboard.com/charts/hot-100/"
SPOTIFY_ENDPOINT_PLAYLIST="https://api.spotify.com/v1/users/"

user_date = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD:")

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/120.0.0.0 Safari/537.36"
}

response = requests.get(f'{BILLBOARD_BASE_URL+user_date}/', headers=headers)
billboard_web_page = response.text

def get_list():
    """This function returns top 100 songs name."""
    soup = BeautifulSoup(billboard_web_page, 'html.parser')
    chart_items = soup.select("li.o-chart-results-list__item h3#title-of-a-story")
    chart_titles = [items.getText().strip() for items in chart_items]
    return chart_titles


try:
    data = get_list()
    print(data)
except requests.exceptions.ConnectTimeout:
    print("Connection timed out, try again.")
    data = get_list()
    print(data)
scope = 'playlist-modify-public playlist-modify-private'

# Checks if our OAuth is valid, and if not , it generates a new token saved in cache file it creates.
# Remember to use same account on your browser and spotify as default email id is used by spotipy upon opening the browser.
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=os.getenv("SPOTIFY_CLIENT_ID"),
                                               client_secret=os.getenv("SPOTIFY_CLIENT_SECRET"),
                                               redirect_uri="https://example.com",
                                               scope=scope,
                                               cache_path="./cache")
                     )
user = sp.current_user() #Important to get details of the current user such as id.

year = user_date.split("-")[0]
track_uris= []

# Gets song URI.
for objects in data:
    result = sp.search(q=f"track:{objects} year:{year}", type='track', limit=1)
    try:
        spotify_uri = result['tracks']['items'][0]['uri']
        track_uris.append(spotify_uri)
    except IndexError:
        print(f"{objects} does not exist in spotify.")


#Creates a playlist.
playlist = sp.user_playlist_create(user=user['id'],
                                   name= f'{user_date} Billboard 100',
                                   public=False,
                                   description=f'This playlist is created as a reminder of time for date-{user_date}'
                                   )
playlist_id = playlist['id']

for songs in track_uris:
    """Add songs to the playlist."""
    sp.playlist_add_items(playlist_id=playlist_id, items=[songs.rsplit(":")[-1]])
print("We did it joe!") # ;)













































































