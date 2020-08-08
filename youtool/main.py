# Given a playlist id from /spotiply/playlists, this script spawns a list of
# youtube video ids
import json
import sys
import os
from HTTPQuery import HTTPQuery

playlist_id = sys.argv[1]
current_dir = os.path.dirname(os.path.realpath(__file__))
with open(f'{current_dir}/../spotiply/playlists/{playlist_id}.json', 'r') as file:
    playlist_json = json.load(file)

youtube_query_data = []
for playlist_item in playlist_json['items']:
    track = playlist_item['track']

    artist = track['artists'][0]['name']
    title = track['name']
    youtube_query_data.append({"query" : f"{artist} {title}", "data" : track})

youtube_video_data = []

for track in youtube_query_data:
    youtube_query = HTTPQuery(track['query'])
    query_response = youtube_query.send_query()
    video_id = youtube_query.filter_response(query_response)
    if video_id != None:
        youtube_video_data.append({'id' : video_id, 'data':track['data']})

ids_file = f"{current_dir}/playlists/{playlist_id}.json"
with open(ids_file, 'w') as file:
    string = json.dumps(youtube_video_data)
    file.write(string)
