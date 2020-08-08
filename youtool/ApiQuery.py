#Issue a youtube query
import json
import os
from googleapiclient.discovery import build

class ApiQuery:
    def __init__(self):
        client_data = self.get_client_data()
        self.client_key = client_data['client_key']
        self.query = build('youtube', 'v3', developerKey=self.client_key).search()

    def get_client_data(self):
        current_dir = os.path.dirname(os.path.realpath(__file__))
        with open(f'{current_dir}/client_data.json', 'r') as file:
            data = json.load(file)
        return data

    def get_query_results(self, q, part='id', order='viewCount', type='video', videoDefinition='high', maxResults=1, videoDuration='any'):
        request = self.query.list(part=part, order=order, q=q, type=type, videoDefinition=videoDefinition, maxResults=maxResults, videoDuration=videoDuration)
        result = request.execute()
        return result

    def get_video_id_from_result(self, result):
        return result['items'][0]['id']['videoId']

    def get_video_id_from_query(self, query, videoDuration='any'):
        query_result = self.get_query_results(query, videoDuration=videoDuration)
        return self.get_video_id_from_result(query_result)
