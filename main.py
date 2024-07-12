from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
CLIENT_ID = "CLIENT_ID"
CLIENT_SECRET = "CLIENT SECRET"
REDIRECT_URI = "http://example.com"


date = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD:\n")

response = requests.get(f"https://www.billboard.com/charts/hot-100/{date}/")
website_html = response.text
soup = BeautifulSoup(website_html, "html.parser")

all_songs_span = soup.select("li ul li h3")
song_titles = [span.getText().strip() for span in all_songs_span]

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        show_dialog=True,
        cache_path="token.txt",
    )
)
user_id = sp.current_user()["id"]
print(user_id)

song_uris = []
year = date.split("-")[0]
for song in song_titles:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    print(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

# Creating a new private playlist in Spotify
playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False)
print(playlist)

# Adding songs found into the new playlist
sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)



