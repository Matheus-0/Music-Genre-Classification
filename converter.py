import os
from pydub import AudioSegment

# Define the path to your "music" folder
music_path = "previews"

# Get a list of all the directories inside the "music" folder
genres = os.listdir(music_path)

# Loop through each genre folder
for genre in genres:
    genre_path = os.path.join(music_path, genre)

    # Get a list of all the .mp3 files inside the genre folder
    mp3_files = [f for f in os.listdir(genre_path) if f.endswith(".mp3")]

    # Loop through each .mp3 file and convert it to .wav
    for mp3_file in mp3_files:
        print(f"{genre}: converting {mp3_file}")

        wav_file = mp3_file.replace(".mp3", ".wav")

        mp3_path = os.path.join(genre_path, mp3_file)
        wav_files_path = os.path.join(genre_path, "wav_files")
        wav_path = os.path.join(wav_files_path, wav_file)

        os.makedirs(wav_files_path, exist_ok=True)

        AudioSegment.from_mp3(mp3_path).export(wav_path, format="wav")
