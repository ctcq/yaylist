#!/bin/bash
basedir=$(dirname ${BASH_SOURCE[0]})
outdir="$PWD";
while getopts "ho:i:" opt; do
  case $opt in
    o)
      outdir="$OPTARG"
      ;;
    i)
      playlist_id="$OPTARG"
      ;;
    h)
      echo "This script takes a spotify playlist id as input and downloads all songs from youtube."
      echo "If no destination directory is given, downloads into current directory."
      echo "Options:"
      echo "-i: Spotify playlist id"
      echo "[-o: Optional. Directory where downloaded files will be stored]"
      exit 1
      ;;
  esac
done

if [ ! -d "$outdir" ]
then
  echo "$outdir is not a directory"
  exit 1
fi

$(python ${basedir}/spotiply/main.py ${playlist_id})

if [ ! -f "${basedir}/spotiply/playlists/${playlist_id}.json" ]
then
  echo "The given playlist id could not be processed." >&2
  exit 1
fi

$(python ${basedir}/youtool/main.py ${playlist_id})
youtube_data="${basedir}/youtool/playlists/${playlist_id}.json"
if [ ! -f "$youtube_data" ]
then
  echo "Youtube API quota exceeded. Not possible to search for video ids..." >&2
  exit 1
fi

$(bash ${basedir}/playlist-dl.sh -i $youtube_data -o $outdir)
