__author__ = 'gazorp'
# coding: utf-8

import os.path
import shutil
from tinytag import TinyTag

# TODO: check mutagen
# TODO: check hsaudiotag
# TODO: add ignore file patterns

FLAC, MP3 = 'FLAC', 'MP3'
# PNG, JPEG = 'PNG', ('JPEG', 'JPG')
BAND_PATTERN = '{0}'
ALB_PATTERN = '{0} - {1}'
TRACK_PATTERN = '{0} - {1}'

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TARGET_DIR = os.path.join(BASE_DIR, 'test_files')
COLLECT_DIR = os.path.join(BASE_DIR, 'collection')


class JukeBox(object):
    """ Finds all music files in path & structures them using by tags """
    def __init__(self, path):
        self.path = path
        self.collection = {}

    def make_collection(self):
        """ Find all music files in self.path & sort them by band
        """
        for top, dirs, files in os.walk(self.path):
            for f in files:
                if f.upper().endswith(MP3) or f.upper().endswith(FLAC):
                    track = TinyTag.get(join(top, f))
                    if not self.collection.get(track.artist):
                        self.collection[track.artist] = []

                    self.collection[track.artist].append(track)

    def replace_band(self, tracklist):
        band_name = tracklist[0].artist
        band_dir_path = join(COLLECT_DIR, BAND_PATTERN.format(band_name))

        albums = {}
        for track in tracklist:
            albums.setdefault(track.album, [])
            albums[track.album].append(track)
        makedir(band_dir_path)
        for a in albums:
            year = albums[a][0].year
            album_dir_path = join(band_dir_path, ALB_PATTERN.format(year, a))
            makedir(album_dir_path)
            for track in albums[a]:
                number = track.track
                track_file_name = TRACK_PATTERN.format(track.track, track.title)
                if FLAC in track._filehandler.name.upper():
                    track_file_name += '.%s' % FLAC.lower()
                else:
                    track_file_name += '.%s' % MP3.lower()
                track_file_path = join(album_dir_path, track_file_name)
                shutil.copy2(track._filehandler.name, track_file_path)

    def replace_collection(self):
        if not self.collection:
            raise Exception("Collection is empty")
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
    input()
