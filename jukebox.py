__author__ = 'gazorp'
# coding: utf-8

import os.path
from tinytag import TinyTag

# TODO: check mutagen
# TODO: check hsaudiotag

FLAC, MP3 = 'FLAC', 'MP3'
PNG, JPEG = 'PNG', ('JPEG', 'JPG')
ALB_PATTERN = '{0} - {1}'

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TARGET_DIR = os.path.join(BASE_DIR, 'test_files')
COLLECT_DIR = os.path.join(BASE_DIR, 'collection')


class JukeBox(object):
    """ Finds all music files in path & structures them using by tags """
    def __init__(self, path):
        self.path = path
        self.collection = {}

    def __str__(self):
        return 'JukeBox object in (%s)' % self.path

    def make_collection(self):
        """ Find and save all music files in self.path

        Create a data dict like:
        collection-[band]-[albums]-[tracklist]-[track 01]
                                  \[year]    |-[track 02]
                                             \-[track 03]
        """
        for top, dirs, files in os.walk(self.path):
            for f in files:
                if f.upper().endswith(MP3) or f.upper().endswith(FLAC):
                    track = join(top, f)
                    tag = TinyTag.get(track)
                    if not self.collection.get(tag.artist):
                        self.collection[tag.artist] = {}

                    if not self.collection[tag.artist].get(tag.album):
                        self.collection[tag.artist][tag.album] = {}

                    if not self.collection[tag.artist][tag.album].get('tracklist'):
                        self.collection[tag.artist][tag.album]['tracklist'] = []

                    if not self.collection[tag.artist][tag.album].get('year'):
                        self.collection[tag.artist][tag.album]['year'] = tag.year

                    self.collection[tag.artist][tag.album]['tracklist'].append(track)

    def run(self):
        self.make_collection()

    def replace_collection(self):
        if not self.collection:
            raise Exception("Collection is empty")

        os.mkdir(COLLECT_DIR)
        for band in self.collection:
            band_dir = join(COLLECT_DIR, band)
            try:
                os.mkdir(band_dir)
            except FileExistsError:
                pass
            for album in self.collection[band]:
                year = self.collection[band][album]['year']
                album_dir = ALB_PATTERN.format(year, album)
                try:
                    os.mkdir(join(band_dir, album_dir))
                except FileExistsError:
                    pass


def join(path, folder):
    return os.path.join(path, folder)


if __name__ == '__main__':
    jukebox = JukeBox(TARGET_DIR)
    jukebox.run()
    jukebox.replace_collection()
    input()
