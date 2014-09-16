import json
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import time
import re
import os
import sys
import datetime as dt
import pprint

# search terms, ariana will get some tweets, reno not too many
search_terms = ['#theresnowayitsanyonebutme']

# Twitter API credentials
sys.path.append('/home/vitale232/Documents/twitter')
from auth import consumer_key, consumer_secret, access_token, access_token_secret

coord_filename = 'isis_coords.csv'
tweet_filename = 'isis_tweets.csv'
# listener
class StdOutListener(StreamListener):
    
    def on_data(self, data):
        if not os.path.isfile(os.path.join(os.getcwd(), coord_filename)):
            c = open(coord_filename, 'w')
            c.write('long, lat\n')
            c.close()

        if not os.path.isfile(os.path.join(os.getcwd(), tweet_filename)):
            c = open(tweet_filename, 'w')
            c.write('tweet, time\n')
            c.close()

        t = open(tweet_filename, 'a+')
        c = open(coord_filename, 'a+')

        # serialize the output
        json_data = json.loads(data)

        # push the tweet text to the display
        # encode to utf-8 to avoid codec errors on Ubuntu
        timestamp = dt.datetime.fromtimestamp(int(json_data['timestamp_ms'])/1000)
        this_tweet = str(json_data['text'].encode('utf-8')).replace('\n', '')

        print(pprint.pprint(json_data))
        print('Tweet at {0}:\n{1}'.format(timestamp, this_tweet))
        t.write('"{0}", {1}\n'.format(this_tweet, timestamp))

        print str(json_data['coordinates']) + '\n'
        if json_data['coordinates'] is not None:
            m = re.search('\[[\d|., \-]*', str(json_data['coordinates']))
            if m is not None:
                c.write(str(m.group()[1:]) + '\n')

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
    time.sleep(86400)
    stream.disconnect()

    end_time = time.strftime('%Y-%m-%d %H:%M:%S')

    print('Program start: {0:>3}'.format(start_time))
    print('Program finish: {0:>2}'.format(end_time))