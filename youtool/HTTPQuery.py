import urllib.parse
import requests

class HTTPQuery:
    def __init__(self, query):
        query = query.replace(" ", "+")
        self.query = urllib.parse.quote(query)
        self.max_attempts = 20

    def send_query(self):
        base_url = "https://www.youtube.com/results?search_query="
        url = f"{base_url}{self.query}"
        self.url = url
        headers = {"User-Agent" : "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; AS; rv:11.0) like Gecko"}
        response = requests.get(url, headers = headers)
        return response.text

    def filter_response(self, response):
        attempts = 0
        current_index = 0
        id_prefix = 'data-video-ids="'
        title_prefix = 'title="'
        while(attempts < self.max_attempts):
            r = response[current_index:]
            #Find the id
            id, i = self.find_assignment_in_string(r, 'data-video-ids="')
            title, i = self.find_assignment_in_string(r[i:], 'title="')
            if True: #self.query_matches_title(title):
                return id
            else:
                attempts += 1
                current_index += i
        return None

    def find_assignment_in_string(self, string, key):
        i = string.find(key)
        start = i + len(key)
        end = start + string[start:].find('"')
        value = string[start:end]
        return value, end

    def query_matches_title(self, title):
        query_split = self.query.split("+")
        title_split = title.split(" ")
        for word in query_split:
            if not word in title_split:
                return False
        return True
