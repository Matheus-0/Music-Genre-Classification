import os
import re


def get_last_music_number(directory):
    regex = re.compile(r'\d+')

    files = os.listdir(directory)

    if len(files) == 0:
        return 0

    last_file = files[-1]

    return int(regex.search(last_file).group(0))
