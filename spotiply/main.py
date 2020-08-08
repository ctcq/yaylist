# This spawns a file /spotiply/playlists
# Contents are metadata from playlist with given argument from commandline
from ApiConnection import ApiConnection
import sys

playlist_id = sys.argv[1]
conn = ApiConnection()
list = conn.get_playlist_tracks_as_json(playlist_id).json()
while (list['next']):
    nextList = ApiConnection().get_oauth().get(list['next']).json()
    list['items'] += nextList['items']
    list['next'] = nextList['next']
conn.dump_json(list, f'playlists/{playlist_id}.json')
