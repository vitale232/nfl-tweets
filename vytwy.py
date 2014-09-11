from twython import TwythonStreamer
from threading import Thread
from twython import Twython
import json
import gdal
import numpy
import time

APP_KEY = 'X8qTLIieJVVOPtQ7mDkERogk1'
APP_SECRET = 'fTIMLM7gMo7NS5qHhw9Su5pVN081lBqw5z7bg6py346JfynNIQ'
OAUTH_TOKEN  = '41348505-4r0d6oQiPpEA2M3EeyHYO6aIUfqbpYCQjeEsYdoVl'
OAUTH_TOKEN_SECRET = 'sBFN7MpYnv0ITtWmDecFFkYNkvWtdOaRCyA3VxYT8Fj4C'

twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

class SourceStreamer(TwythonStreamer):
    def __init__(self, *args):
        super(SourceStreamer, self).__init__(*args)
        self.coords = {
            'android': [], 'iOS': [],
        }

    def on_success(self, data):
        """If tweet has geo-information, add it to the list."""
        try:
            source = data['source']
            if 'Android' in source:
                self.coords['android'].append(data['geo']['coordinates'])
            elif 'iOS' in source or 'iPhone' in source or 'iPad' in source:
                self.coords['iOS'].append(data['geo']['coordinates'])
        except (AttributeError, KeyError, TypeError):
            pass

    def on_error(self, status_code, data):
        """On error, print the error code and disconnect ourselves."""
        print('Error: {0}'.format(status_code))
        self.disconnect()

class StreamThread(Thread):
    def run(self):
        self.stream = SourceStreamer(
            APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET
        )
        self.stream.statuses.filter(locations='-180,-90,180,90')

t = StreamThread()
t.daemon = True
t.start()
time.sleep(10)

print t
# twitter.update_status(status='Hello, world from #Twython.')