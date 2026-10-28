import os

from loguru import logger
import mutagen
from tqdm import tqdm

TITLE = "title"
ARTIST = "artist"

extensions = ('mp3', 'wav', 'm4a', 'flac')

def get_song_count(directory) -> dict[str, list[str]]:
    songs: dict[str, list[str]] = {}
    file_paths = []
    for dirpath, _, filenames in os.walk(directory):
        for filename in filenames:
            file_paths.append(os.path.join(dirpath, filename))

    for path in tqdm(file_paths):
        if path.endswith(extensions):
            file = mutagen.File(path, easy=True)
            try:
                title = file[TITLE][0]
                artist = file[ARTIST][0]

                if title not in songs.keys():
                    songs[title] = [artist]
                else:
                    songs[title].append(artist)
            except KeyError:
                logger.warning(f"{path} missing artist or title")
    return songs

def count_songs(songs: dict[str, list[str]]) -> None:
    logger.info(f"Total unique song names: {len(songs)}")
    sorted_songs = sorted(songs.items(), key=lambda item: len(item[1]), reverse=True)
    logger.info("Top 20:")
    for title, artists in sorted_songs[:20]:
        logger.info(f"- {title} - {len(artists)} {artists}")


def main(directory: str):
    songs = get_song_count(directory)
    count_songs(songs)



if __name__ == '__main__':
    main("TODO")