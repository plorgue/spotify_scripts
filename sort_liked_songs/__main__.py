import spotipy
from spotipy.oauth2 import SpotifyOAuth

# ============================
# CONFIGURATION
# ============================
CLIENT_ID = ""
CLIENT_SECRET = ""
REDIRECT_URI = "http://localhost:8888/callback"
SCOPE = "user-library-read playlist-modify-private playlist-modify-public"

# Mapping entre les années et les IDs des playlists
YEAR_TO_PLAYLIST_ID = {
    2025: "",
    2024: "",
    2023: "",
    2022: "",
    2021: "",
    2020: "",
    2019: "",
    2018: "",
    2017: "",
    2016: "",
}

# ============================
# AUTHENTIFICATION
# ============================
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    scope=SCOPE
))

# ============================
# RÉCUPÉRATION DES TITRES AIMÉS
# ============================
def get_liked_tracks():
    """Récupère tous les titres likés par l'utilisateur"""
    liked_tracks = []
    results = sp.current_user_saved_tracks(limit=50)

    while results:
        for item in results['items']:
            track = item['track']
            added_at = item['added_at']  # Date d'ajout du titre
            liked_tracks.append({
                "id": track['id'],
                "name": track['name'],
                "artist": track['artists'][0]['name'],
                "added_at": added_at
            })

        # Pagination : passer à la page suivante
        if results['next']:
            results = sp.next(results)
        else:
            break

    return liked_tracks

# ============================
# TRI ET AJOUT AUX PLAYLISTS
# ============================
def sort_and_add_to_playlists(liked_tracks):
    """Trie les titres par année et les ajoute aux playlists correspondantes"""
    for track in liked_tracks:
        # Récupérer l'année d'ajout
        year = int(track['added_at'][:4])

        # Trouver la playlist correspondante
        playlist_id = YEAR_TO_PLAYLIST_ID.get(year)

        if playlist_id:
            print(f"Ajout de {track['name']} ({track['artist']}) à la playlist {year}")
            sp.playlist_add_items(playlist_id, [track['id']])
        else:
            print(f"Aucune playlist trouvée pour l'année {year} (titre : {track['name']})")

# ============================
# MAIN
# ============================
if __name__ == "__main__":
    print("Récupération des titres likés...")
    liked_tracks = get_liked_tracks()
    print(f"{len(liked_tracks)} titres likés récupérés.")

    print("Ajout des titres aux playlists...")
    sort_and_add_to_playlists(liked_tracks)
    print("Terminé !")
