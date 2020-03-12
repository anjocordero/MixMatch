import requests

import spotipy
import spotipy.util as util

from env import SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI,\
    max_track_limit, scope
from config import username, BPM, playlist_name,\
    energy_minimum, danceability_minimum, round_to_tens

class Song():
    '''
    Class which contains the relevant information from a Spotify audio features
    API request.
    '''

    def __init__(self, features):
        self.danceability = features['danceability']
        self.energy = features['energy']
        self.tempo = features['tempo']
        self.id = features['id']

def convert_round():
    if round_to_tens:
        return -1
    else:
        return 0

def get_all_saved_tracks(spotify):
    '''
    Since the GET request has a limit of 50, this function appends the user's
    entire saved collection to a single object.
    '''

    results = spotify.current_user_saved_tracks(limit=max_track_limit)
    saved = results['items']
    while (results['next']):
        results = spotify.next(results)
        saved.extend(results['items'])

    return saved


def process_songs(spotify, saved):
    '''
    Takes the song features returned from the Spotify API and stores the
    relevant information
    '''
    songs = []
    ids = []

    for item in saved:
        id_number = item['track']['id']
        ids.append(id_number)

    # audio features returns a list, can take multiple id numbers up to 100
    offset = 0
    features = []

    while (offset < len(ids)):
        features.extend(spotify.audio_features(ids[offset:offset+100]))
        offset += 100

    for feature in features:
        song = Song(feature)
        songs.append(song)

    return songs


def main():
    round_to_tens = convert_round()
    token = util.prompt_for_user_token(
        username=username,
        scope=scope,
        client_id=SPOTIPY_CLIENT_ID,
        client_secret=SPOTIPY_CLIENT_SECRET,
        redirect_uri=SPOTIPY_REDIRECT_URI
    )

#token = util.prompt_for_user_token(username=username,scope=scope,client_id=SPOTIPY_CLIENT_ID,client_secret=SPOTIPY_CLIENT_SECRET,redirect_uri=SPOTIPY_REDIRECT_URI)

    if token:
        spotify = spotipy.client.Spotify(auth=token)
        user_id = spotify.me()['id']

        saved = get_all_saved_tracks(spotify)

        songs = process_songs(spotify, saved)

        playlist = spotify.user_playlist_create(
            user_id, playlist_name, public=False,
            description="Playlist created by Mix Match at " + str(BPM) + " BPM."
        )

        #playlist = spotify.user_playlist_create(user_id, playlist_name, public=False, description="Playlist created by Mix Match at " + str(BPM) + " BPM.")

        matches = [song.id for song in songs if 
            round(song.tempo, round_to_tens) == BPM and
            song.energy >= energy_minimum and 
            song.danceability >= danceability_minimum
            ]

        spotify.user_playlist_add_tracks(user_id, playlist['id'], matches)


if __name__ == "__main__":
    main()
