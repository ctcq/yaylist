# yaylist

This is a small, hacky tool to automatically search and downlaod all titles from a *spotify* playlists via the awsome [youtube-dl](https://github.com/ytdl-org/youtube-dl) tool.

## Requirements
This should run on any Linux Machine having installed `python 3`. 

1. Firstly, you need access to the Spotify API to be able to browse playlist data. You can register [here](https://developer.spotify.com/). I give no warranty on whether your use of my program complies with Spotify's *Terms of Use*.
2. Enter your `client_id` and `client_key` into the `spotiply/client_data.json`. You also need to enable OAuth and enter the `refresh_token` you got after authorization.
3. Install [youtube-dl](https://github.com/ytdl-org/youtube-dl).

## Usage
Clone this repository, navigate into it and execute

``` bash
sh yaylist.sh -i <spotify-playlist-id> -o <output-dir>
```
