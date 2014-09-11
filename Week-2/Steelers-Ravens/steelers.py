import json
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import time
import re
import os
import sys

# search terms, ariana will get some tweets, reno not too many
search_terms = ['steelers']

# Twitter API credentials
sys.path.append('/home/vitale232/Documents/twitter')
from auth import consumer_key, consumer_secret, access_token, access_token_secret


# listener
class StdOutListener(StreamListener):
    
    def on_data(self, data):
        if not os.path.isfile(os.path.join(os.getcwd(), 'steelers.csv')):
            c = open('steelers.csv', 'w')
            c.write('long, lat\n')
            c.close()

        t = open('steelers.csv', 'a+')
        c = open('steelers.csv', 'a+')
        # serialize the output
        json_data = json.loads(data)
        # push the tweet text to the display
        # encode to utf-8 to avoid codec errors on Ubuntu
        print json_data['text'].encode('utf-8')
        t.write(str(json_data['text'].encode('utf-8')) + '\n')
        print json_data['coordinates']
        if json_data['coordinates'] is not None:
            m = re.search('-[\d|., ]*', str(json_data['coordinates']))
            if m is not None:
                print(m.group())
                c.write(str(m.group()) + '\n')

        # append each json object to the list
        t.close()
        c.close()
        return True

    def on_error(self, status):
        print('ERROR: {0}'.format(status))
        print(time.strftime('%Y-%m-%d %H:%M:%S'))

if __name__ == '__main__':
    start_time = time.strftime('%Y-%m-%d %H:%M:%S')
    print('Starting program at {0}'.format(start_time))

    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)
    stream.filter(track=search_terms, async=True)
    time.sleep(1)
    stream.disconnect()

    end_time = time.strftime('%Y-%m-%d %H:%M:%S')

    print('Program start: {0:>3}'.format(start_time))
    print('Program finish: {0:>2}'.format(end_time))