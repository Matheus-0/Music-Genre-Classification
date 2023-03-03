import requests
from tqdm import tqdm
import urllib.request

id_ = input('Playlist ID: ')

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

for i in range(len(tracks)):
    try:
        urllib.request.urlretrieve(tracks[i]['preview'], f'./previews/{playlist_title}/{i}.mp3')
    except ValueError:
        pass
    finally:
        progress.update()
