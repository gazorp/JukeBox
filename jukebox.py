__author__ = 'gazorp'
# coding: utf-8

import os.path
import shutil
import threading
from tinytag import TinyTag

# TODO: check mutagen
# TODO: check hsaudiotag
# TODO: отдельная функция копирования с обработкой символов

FLAC, MP3 = 'FLAC', 'MP3'
COVERS = (
    'COVER.JPG', 'COVER.JPEG', 'FOLDER.JPG', 'FOLDER.JPEG'
)

ALBUM_PATTERN = '{year} - {title}'
BAND_PATTERN = '{title}'
TRACK_PATTERN = '{number} - {title}'


class JukeBox(object):

    def __init__(self, path):
        self.path = path
        self.collection = {}

    def make_collection(self):
        """
        Find all .mp3/.flac in self.path and write to self.collection
        separated by artists
        """
        for top, dirs, files in os.walk(self.path):
            for f in files:
                if f.upper().endswith(MP3) or f.upper().endswith(FLAC):
                    track = TinyTag.get(join(top, f), image=True)
                    self.collection.setdefault(track.artist, [])
                    self.collection[track.artist].append(track)

        if not self.collection:
            raise Exception('There is no music files in folder')

    def find_album_cover(self, tracklist):
        """
        Try to find album cover and move it to new folder

        If tracks now located in one place, try to find cover file.

        :param tracklist: list of TinyTag objects of album
        :return path to album cover file
        """
        path = os.path.dirname(tracklist[0]._filehandler.name)
        for track in tracklist:
            if path != os.path.dirname(track._filehandler.name):
                return None
        files = os.listdir(path)
        cover_file = ''
        count = 0
        for f in files:
            if f.upper() in COVERS:
                cover_file = join(path, f)
                count += 1
        if count == 1:
            return cover_file
        return None

    def replace_band(self, tracklist):
        """
        Replaced all music of band to COLLECT_DIR/BAND_TITLE/(albums)

        :param tracklist: list of TinyTag objects of tracks of this band
        """
        albums = {}
        artist_title = tracklist[0].artist
        artist_dir_path = join(
            COLLECT_DIR,
            BAND_PATTERN.format(
                title=artist_title
            )
        )
        makedir(artist_dir_path)

        # Separate all tracks to albums
        for track in tracklist:
            albums.setdefault(track.album, [])
            albums[track.album].append(track)

        # Create folder for each album
        for album in albums:
            year = albums[album][0].year
            album_dir_path = join(
                artist_dir_path,
                ALBUM_PATTERN.format(
                    year=year,
                    title=album
                )
            )
            # Edit folder name if it's EP
            if album_dir_path.endswith(' Ep'):
                album_dir_path = album_dir_path[:-3] + ' EP'
            makedir(album_dir_path)

            # Try to find a cover
            album_cover = self.find_album_cover(albums[album])
            if album_cover:
                cover = join(album_dir_path, 'cover.jpg')
                shutil.copy2(album_cover, cover)

            # Name tracks by pattern
            for track in albums[album]:
                number = track.track  # TODO: лямбда-выражения
                track_file_name = TRACK_PATTERN.format(
                    number=number,
                    title=track.title.title()
                )
                if FLAC in track._filehandler.name.upper():
                    track_file_name += '.%s' % FLAC.lower()
                else:
                    track_file_name += '.%s' % MP3.lower()

                # Move track to album_dir_path
                track_file_path = join(album_dir_path, track_file_name)
                shutil.copy2(track._filehandler.name, track_file_path)

    def replace_collection(self):
        """
        Move all the music to COLLECT_DIR/(bands)
        """
        if not self.collection:
            raise Exception("Nothing to replace")
        makedir(COLLECT_DIR)

        all_bands = len(self.collection)
        count = 0
        for band in self.collection:
            progress = int(count / all_bands * 20)
            print('/' * progress, end='')
            print('%i of %i' % (count, len(self.collection)), end='')
            print('_' * (20 - progress), '(%s)' % (band, ))
            self.replace_band(self.collection[band])
            count += 1
        print('> All bands replaced <')

    def run(self):
        self.make_collection()
        self.replace_collection()


def join(path, folder):
    return os.path.join(path, folder)


def makedir(path):
    if os.path.exists(path):
        if not os.path.isdir(path):
            raise Exception('Path %s is not a directory' % path)
        return
    os.mkdir(path)


if __name__ == '__main__':
    jukebox = JukeBox(TARGET_DIR)
    jukebox.run()
    print('Finish')
