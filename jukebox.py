__author__ = 'gazorp'
# coding: utf-8

import os.path
from tinytag import TinyTag
from os import listdir
"""
TODO: check mutagen
TODO: check hsaudiotag
TODO: check tinytag
"""

FLAC, MP3 = 'FLAC', 'MP3'

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TARGET_DIR = os.path.join(BASE_DIR, 'test')


class JukeBox(object):
    """ Finds all music files in path & structures them to tree using by tags """
    def __init__(self, path):
        self.path = join(TARGET_DIR, path)
        self.tracks = []
        self.collection = {}

    def __str__(self):
        return 'JukeBox object in %s' % self.path or None

    def aggregate_tracks(self):
        """ Find and save all music files in self.path """
        tracks = []
        for top, dirs, files in os.walk(self.path):
            for f in files:
                if f.upper().endswith(MP3) or f.upper().endswith(FLAC):
                    tracks.append(join(top, f))

    def run(self):
        pass


def join(path, folder):
    return os.path.join(path, folder)


if __name__ == '__main__':
    jukebox = JukeBox(TARGET_DIR)
    jukebox.run()
