import json
import os

import requests
from tqdm import tqdm
import urllib.request

from utils import get_last_music_number

id_ = input('Playlist ID: ')
genre = input('Genre: ')

URL = f'https://api.deezer.com/playlist/{id_}'
response = requests.get(URL).json()
tracks = response['tracks']['data']
playlist_title = response['title']

progress = tqdm(
    desc=f'Downloading previews from playlist "{playlist_title}"',
    total=len(tracks),
    bar_format='{desc}: {percentage:3.0f}% |{bar}| [{elapsed} < {remaining}]',
    colour='green'
)

genre_directory = os.path.join(os.getcwd(), 'previews', genre)
os.makedirs(genre_directory, exist_ok=True)

with open('downloaded_song_ids.json', 'r') as f:
    content = json.loads(f.read())

downloaded_song_ids = content.get(genre, [])

count = get_last_music_number(genre_directory) + 1

repeated_songs = []

for i in range(len(tracks)):
    try:
        song_id = tracks[i]['id']
        preview_url = tracks[i]['preview']

        if song_id not in downloaded_song_ids:
            downloaded_song_ids.append(song_id)

            file_number = str(count).zfill(5)

            file = os.path.join(genre_directory, f'{genre}.{file_number}.mp3')

            if not os.path.isfile(file):
                urllib.request.urlretrieve(preview_url, file)

                count += 1
        else:
            repeated_songs.append(tracks[i]['title'])
    except ValueError:
        pass
    finally:
        progress.update()

content[genre] = downloaded_song_ids

with open('downloaded_song_ids.json', 'w') as f:
    f.write(json.dumps(content, indent=2))


if len(repeated_songs) > 0:
    print('Repeated songs:\n')

    for song in repeated_songs:
        print(song)
