__author__ = 'gazorp'
# coding: utf-8


class MusicRepo:
    tracks = []

    fields = (
        'artist', 'albumartist', 'album', 'title',
        'track', 'duration', 'filesize', 'bitrate',
        'channels', 'genre', 'samplerate', 'year'
    )

    def from_tinytag(self, tinytag):
        tag = tinytag.__dict__
        return {key: tag[key] for key in self.fields}

    def add(self, track):
        self.tracks.append(track)

    def get_tracks(self):
        return self.tracks

    def dump(self):
        json = dict()
        json['tracks'] = self.tracks
        json['total_tracks'] = len(self.tracks)


class MusicStats:
    MP3, FLAC = (
        'mp3', 'flac'
    )

    def __init__(self, repo):
        self.music_repo = repo

    def add_band(self):
        pass

    def dump_to_json(self, json_output):
        pass

    def create_from_json(self, json_input):
        pass

    def get_full_stats(self):
        pass
