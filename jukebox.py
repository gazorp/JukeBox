__author__ = 'gazorp'
# coding: utf-8

import os.path
import shutil
from tinytag import TinyTag

# TODO: check mutagen
# TODO: check hsaudiotag
# TODO: add ignore file patterns

FLAC, MP3 = 'FLAC', 'MP3'
COVERS = (
    'COVER.JPG', 'COVER.JPEG', 'FOLDER.JPG', 'FOLDER.JPEG'
)

ALB_PATTERN = '{year} - {title}'
BAND_PATTERN = '{title}'
TRACK_PATTERN = '{number} - {title}'

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TARGET_DIR = os.path.join(BASE_DIR, 'test_folders')
COLLECT_DIR = os.path.join(BASE_DIR, 'collection')


class JukeBox(object):
    """ Finds all music files in path & structures them using by tags
    """
    def __init__(self, path):
        self.path = path
        self.collection = {}

    def make_collection(self):
        """ Find all music files in self.path & sort them by band
        """
        for top, dirs, files in os.walk(self.path):
            for f in files:
                if f.upper().endswith(MP3) or f.upper().endswith(FLAC):
                    track = TinyTag.get(join(top, f), image=True)
                    self.collection.setdefault(track.artist, [])
                    self.collection[track.artist].append(track)

        if not self.collection:
            raise Exception('There is no music files in this folder\nCollection is empty')

    def find_album_cover(self, tracklist):
        """
        Try to find album cover and move it to new folder

        :param tracklist: list of TinyTag objects of album

        If tracks now located in one place, try to find cover file.
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

    def replace_band(self, tracklist):
        """
        Replaced all music of band to COLLECT_DIR/BAND_TITLE/(albums)

        :param tracklist -  list of TinyTag objects of this band
        """
        albums = {}
        band_name = tracklist[0].artist
        band_dir_path = join(
            COLLECT_DIR,
            BAND_PATTERN.format(
                title=band_name
            )
        )
        makedir(band_dir_path)

        # Separate all tracks to albums
        for track in tracklist:
            albums.setdefault(track.album, [])
            albums[track.album].append(track)

        # Create folder for each album
        for album in albums:
            year = albums[album][0].year
            album_dir_path = join(
                band_dir_path,
                ALB_PATTERN.format(
                    year=year,
                    title=album.title()
                )
            )
            makedir(album_dir_path)
            album_cover = self.find_album_cover(albums[album])
            if album_cover:
                cover = join(album_dir_path, 'cover.jpg')
                shutil.copy2(album_cover, cover)

            # Name tracks by pattern
            for track in albums[album]:
                number = track.track  # TODO: лямбда-выражения
                track_file_name = TRACK_PATTERN.format(
                    number=number,
                    title=track.title
                )
                if FLAC in track._filehandler.name.upper():
                    track_file_name += '.%s' % FLAC.lower()
                else:
                    track_file_name += '.%s' % MP3.lower()

                # Move track to album_dir_path
                track_file_path = join(album_dir_path, track_file_name)
                shutil.copy2(track._filehandler.name, track_file_path)

    def replace_collection(self):
        """ Remove all the music to COLLECT_DIR/(bands)
        """
        if not self.collection:
            raise Exception("Can't replace collection\nCollection is empty")
        makedir(COLLECT_DIR)

        for band in self.collection:
            self.replace_band(self.collection[band])

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
    input('Finish')
