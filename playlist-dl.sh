#!/bin/bash

# This script downloads all youtube links contained in a given file youtool/playlist/file.json
outdir="$PWD";
infile=""
while getopts "ho:i:" opt; do
  case $opt in
    o)
      outdir="$OPTARG"
      ;;
    i)
      infile="$OPTARG"
      ;;
    h)
      echo "This script downloads all youtube videos specified in a given json file."
      echo "If no destination directory is given, downloads into current directory."
      echo "Options:"
      echo "-i: Input file spawned by /youtool/main.py"
      echo "[-o: Directory where downloaded files will be stored]"
      exit 1
      ;;
  esac
done

if [ ! -f "${infile}" ]
then
  echo "File $infile not found"
  exit 1
fi

if [ ! -d "$outdir" ]
then
  echo "$outdir is not a directory"
  exit 1
fi

echo "Downloading playlist to destination folder '${outdir}'"

# Read json file and dump into bash array
declare -a yt_ids
l="$(jq length $infile)"
for ((i=0;i<l;i++))
do
  song_name="$(jq .[$i].data.name $infile)"
  song_name="${song_name//\"/""}"
  artist_name="$(jq .[$i].data.artists[0].name $infile)"
  artist_name="${artist_name//\"/""}"
  echo "Downloading $artist_name - $song_name"
  yt_id="$(jq .[$i].id $infile)"
  yt_id="${yt_id//\"/""}"
  yt_url="https://www.youtube.com/watch?v=${yt_id}"
  #yt_url="${yt_url//\"/""}" #Strip quote characters
  outfile="${outdir}/${song_name}.%(ext)s"
  echo "Downloading video '${yt_url}'"
  "$(youtube-dl -o "${outfile}" -f 251 --add-metadata -x --audio-format mp3 $yt_url)"
done
