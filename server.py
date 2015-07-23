#!/usr/bin/env python2

from __future__ import print_function
from gmusicapi import Mobileclient
import collections
import sys
import toml
import gst
import pygst
import time
import zmq
import argparse

class MusicQueue:
    def __init__(self, api):
        self.track_ids = []
        self.position = 0
        self.player = gst.element_factory_make("playbin", "player")
        self.current = {}
        self.api = api
        self.size = 0

    def on_tag(bus, msg):
        taglist = msg.parse_tag()
        print('on_tag:')
        for key in taglist.keys():
            print('\t%s = %s') % (key, taglist[key])

    def elapsed_time(self):
        return time.time() - self.starttime

    def play_song(self):
        self.player.set_state(gst.STATE_PLAYING)

    def pause_song(self):
        self.player.set_state(gst.STATE_PAUSED)

    def stop_song(self):
        self.player.set_state(gst.STATE_NULL)

    def get_id(self, query, command):
        results = self.api.search_all_access(query, 1)

        if command == 'albumquery':
            album_id = results["album_hits"][0]['album']['albumId']
            return album_id
        elif command == 'trackquery':
            track_id = results["song_hits"][0]['track']['nid']
            return track_id

    def set_track(self, track_id):
        track = self.api.get_track_info(track_id)
        self.current = track

        streamurl = self.api.get_stream_url(track_id)
        waittime = (float(track['durationMillis']) / 1000)

        self.player.set_property('uri', streamurl)

        bus = self.player.get_bus()
        bus.enable_sync_message_emission()
        bus.add_signal_watch()
        bus.connect('message::tag', self.on_tag)

        print("Artist: "+track['artist'].encode('ascii'))
        print("Track: "+track['title'].encode('ascii'))
        print("Duration: %0.2f\n" % (waittime/60))

        self.play_song()

    def set_album(self, album_id):
        album_info = self.api.get_album_info(album_id)
    
        for track in album_info['tracks']:
            self.track_ids.append(track['nid'])
            self.size = len(album_info['tracks'])

        print('\nAlbum: '+album_info['name']+'\n')

        for track in album_info['tracks']:
            self.set_track(track['nid'])
            print(self.player.get_state())
            time.sleep(waittime + 1)

    def add_album(self, album_id):
        album_info = self.api.get_album_info(album_id)
    
        for track in album_info['tracks']:
            self.track_ids.append(track['nid'])
            self.size = self.size + len(album_info['tracks'])

        print('\nAdding Album: '+album_info['name']+'\n')

    def add_track(self, track_id):
        track = self.api.get_track_info(track_id)

        self.track_ids.append(track['nid'])
        self.size = self.size + 1

        print('\nAdding Track: '+track['title']+'\n')

def main():
    with open('./config.toml') as conffile:
        config = toml.loads(conffile.read())

    auth = config['auth']

    try:
        api = Mobileclient()
        api.login(auth['email'], auth['password'], auth['deviceid'])
    except:
        pass

    mq = MusicQueue(api)

    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind('tcp://127.0.0.1:6666')

    print('Starting server...')

    while True:
        msg = socket.recv_json()
        print(msg)
        if msg['command'] == 'what':
            print(mq.current)
            socket.send_string(msg['command']+' recieved')
        elif msg['command'] == 'albumquery':
            album_id = mq.get_id(msg['query'], 'albumquery')
            if 'queue' not in msg:
                mq.stop_song()
                mq = MusicQueue(api)
            else:
                mq.add_album(album_id)

            mq.set_album(album_id)
            mq.play_song()

            socket.send_string(msg['command']+' recieved')
        elif msg['command'] == 'trackquery':
            track_id = mq.get_id(msg['query'], 'trackquery')
            if 'queue' not in msg:
                mq.stop_song()
                mq = MusicQueue(api)
            else:
                mq.add_track(track_id)

            mq.set_track(track_id)
            mq.play_song()

            socket.send_string(msg['command']+' recieved')
        elif msg['command'] == 'pause':
            mq.pause_song()

            socket.send_string(msg['command']+' recieved')
        elif msg['command'] == 'stop':
            mq.stop_song()

            socket.send_string(msg['command']+' recieved')
        elif msg['command'] == 'play':
            mq.play_song()

            socket.send_string(msg['command']+' recieved')
        elif msg['command'] == 'skip':
            mq.stop_song()
            print(mq.track_ids)
            print(mq.position)
            if (mq.position + 1) < mq.size:
                mq.position = mq.position + 1
                mq.set_track(mq.track_ids[mq.position])

            socket.send_string(msg['command']+' recieved')
        elif msg['command'] == 'prev':
            mq.stop_song()
            print(mq.track_ids)
            print(mq.position)
            if (mq.position + 1) >= 0:
                mq.position = mq.position - 1
                mq.set_track(mq.track_ids[mq.position])

            socket.send_string(msg['command']+' recieved')
        elif msg['command'] == 'halt':
            print('Halting server...')

            socket.close()
            exit(0)

if __name__ == "__main__":
    main()
