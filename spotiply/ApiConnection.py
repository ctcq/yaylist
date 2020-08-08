import json
import requests
from requests_oauthlib import OAuth2Session
import base64
import time
import os
class ApiConnection(object):
    def __init__(self):
        client_data = self.get_client_data()
        self.client_id = client_data['client_id']
        self.client_key = client_data['client_key']
        self.auth_key = client_data['auth_key']
        self.refresh_token = client_data['refresh_token']
        self.redirect_uri = client_data['redirect_uri']
        self.auth_expires = 0

    def get_client_data(self):
        current_dir = os.path.dirname(os.path.realpath(__file__))
        with open(f'{current_dir}/client_data.json', 'r') as file:
            data = json.load(file)
        return data

    def build_authorization(self):
        string_encoded = (self.client_id + ":" + self.client_key).encode()
        return base64.b64encode(string_encoded).decode()

    def authorize(self):
        url = 'https://accounts.spotify.com/api/token'
        oauth = OAuth2Session(self.client_id, redirect_uri=self.redirect_uri)
        oauth.authorization_url(url)

        response = oauth.fetch_token(url, client_secret=self.client_key, code=self.auth_key)

        self.access_token = response['access_token']
        self.refresh_token = response['refresh_token']
        self.auth_expires = time.time() + int(response['expires_in'])
        self.update_json()
        return oauth

    def refresh_access_token(self):
        url = 'https://accounts.spotify.com/api/token'
        oauth = OAuth2Session(self.client_id, redirect_uri=self.redirect_uri)
        oauth.authorization_url(url)

        response = oauth.refresh_token(url, client_secret=self.client_key, client_id=self.client_id, refresh_token=self.refresh_token)

        self.access_token = response['access_token']
        if 'refresh_token' in response:
            self.refresh_token = response['refresh_token']
            self.update_json()

        self.auth_expires = time.time() + int(response['expires_in'])
        return oauth

    def get_oauth(self):
        if time.time() > self.auth_expires:
            return self.refresh_access_token()
        return self.authorize()

    def get_playlist_tracks_as_json(self, playlist_id):
        oauth = self.get_oauth()
        url = f'https://api.spotify.com/v1/playlists/{playlist_id}/tracks'
        return oauth.get(url)

    def dump_json(self, obj, filename):
        string = json.dumps(obj)
        dir = os.path.dirname(os.path.realpath(__file__))
        with open(dir + "/" + filename, 'w') as file:
            file.write(string)

    def update_json(self):
        self.dump_json(self.__dict__, 'client_data.json')
