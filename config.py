# Write your Spotify username here
username = "126860044"

# Change these variables to filter which songs appear in the playlist.
BPM = 150
# 0.0 < X < 1.0
energy_minimum = 0.7
danceability_minimum = 0.6

# True if you want to round song BPMs to the tens digit, False if ones digit
round_to_tens = True

# Change whether or not to search through followed playlists
search_playlists = True

# Name of the Spotify playlist to be created
playlist_name = "Mix Match: " + str(BPM) + " BPM"
if round_to_tens:
    playlist_name += "(ish)"