__author__ = 'gazorp'
# coding: utf-8

from tinytag import TinyTag


class Album:
    def __init__(self):
        self.band_title = None
        self.year = None
        self.title = None
        self.genre = None
        self.cover = {}
        self.quality = None
        self.folder = None

    def add_track(self, track):
        pass

    def set_cover(self, file, size, type, res):
        pass

    def get_cover_size(self):
        pass

    def to_json(self):
        pass


class Band:
    def __init__(self):
        self.title = None
        self.albums = []
        self.folder = None

    def add_album(self, album):
        pass

    def to_json(self):
        pass


class MusicStats:
    def __init__(self):
        self.bands = []

    def add_band(self):
        pass

    def dump_to_json(self, json_output):
        pass

    def create_from_json(self, json_input):
        pass
