import spotipy
from spotipy.oauth2 import SpotifyOAuth

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    # https://developer.spotify.com/dashboard
    client_id="...",
    client_secret="...",
    redirect_uri="http://127.0.0.1:8080/callback",
    scope="playlist-read-private user-read-private")
)
PLAYLIST_ID = "2pwdfmrLlI6aMgs6AhnKOa" # ID вашего плейлиста

print("Сканирую плейлист...")
print("-" * 50)

def check_tracks(results):
    for item in results['items']:
        if not item or not item.get('track'):
            continue

        track = item['track']
        name = track.get('name', 'Unknown')
        artists = ", ".join([a['name'] for a in track.get('artists', [])])
        uri = track.get('uri')
        if track.get('is_local'):
            continue

        is_playable = track.get('is_playable')

        if is_playable is False:
            print(f"[X] НЕДОСТУПЕН: {artists} - {name}")
            print(f"    URI: {uri}")
            print("-" * 20)

results = sp.playlist_tracks(PLAYLIST_ID, market="from_token")
check_tracks(results)

while results['next']:
    results = sp.next(results)
    check_tracks(results)