__author__ = 'gazorp'
# coding: utf-8

from tinytag import ID3, Flac
import json

MP3, FLAC = ('mp3', 'flac')


class MusicHelper:
    @staticmethod
    def identify_format(tinytag):
        format = type(tinytag)
        if format is ID3:
            return MP3
        elif format is Flac:
            return FLAC
        return None

    @staticmethod
    def is_mp3(file):
        return file.lower().endswith(MP3)

    @staticmethod
    def is_flac(file):
        return file.lower().endswith(FLAC)


class MusicRepo:
    tracks = []
    tracks_total = 0

    def from_tinytag(self, tinytag):
        fields = (
            'artist', 'albumartist', 'album', 'title',
            'track', 'duration', 'filesize', 'bitrate',
            'channels', 'genre', 'samplerate', 'year'
        )
        tag = tinytag.__dict__
        track = {key: tag[key] for key in fields}
        track['format'] = MusicHelper.identify_format(tinytag)
        return track

    def add(self, track):
        self.tracks.append(track)
        self.tracks_total += 1

    def get_tracks(self):
        return self.tracks

    def dump(self, dumpfile):
        data = dict()
        data['tracks'] = self.tracks
        data['total_tracks'] = self.tracks_total
        json.dump(data, open(dumpfile, 'w'))

    def from_json(self, dumpfile):
        data = json.load(open(dumpfile, 'r'))
        self.tracks = data['tracks']
        self.tracks_total = data['total_tracks']


class MusicStats:

    def __init__(self, repo):
        self.repo = repo

    def add_band(self):
        pass

    def get_full_stats(self):
        pass

    def get_percentage_of(self, value):
        if value is not 0:
            return "{0:.2f}%".format(value / self.repo.tracks_total * 100)
        return '0%'

    def get_flac_percentage(self):
        flac_tracks = 0
        for track in self.repo.get_tracks():
            if track['format'] == FLAC:
                flac_tracks += 1
        return self.get_percentage_of(flac_tracks)

    def get_mp3_percentage(self):
        mp3_tracks = 0
        for tracks in self.repo.get_tracks():
            if tracks['format'] == MP3:
                mp3_tracks += 1
        return self.get_percentage_of(mp3_tracks)
