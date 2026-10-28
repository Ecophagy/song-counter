import os

from loguru import logger
import mutagen

TITLE = "title"
ARTIST = "artist"

extensions = ('mp3', 'wav', 'm4a', 'flac')

def get_song_count(directory) -> dict[str, list[str]]:
    songs: dict[str, list[str]] = {}

    for path, directories, files in os.walk(directory):
        for filename in files:
            if filename.endswith(extensions):
                file = mutagen.File(os.path.join(path, filename))
                try:
                    title = file[TITLE][0]
                    artist = file[ARTIST][0]

                    if title not in songs.keys():
                        songs[title] = [artist]
                    else:
                        songs[title].append(artist)
                except KeyError:
                    logger.warning(f"{filename} missing artist or title")
    return songs

def analyse_songs(songs: dict[str, list[str]]):
    logger.info(f"Total unique song names: {len(songs)}")
    sorted_songs = sorted(songs.items(), key=lambda item: len(item[1]), reverse=True)
    logger.info("Top 5:")
    for title, artist in sorted_songs[:5]:
        logger.info(f"- {title} - {artist}")


def main(directory: str):
    songs = get_song_count(directory)
    analyse_songs(songs)



if __name__ == '__main__':
    main("TODO")