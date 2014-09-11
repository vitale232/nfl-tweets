import json
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import time
import re
import os
import sys
import datetime as dt

# search terms, ariana will get some tweets, reno not too many
search_terms = ['ravens']

# Twitter API credentials
sys.path.append('/home/vitale232/Documents/twitter')
from auth import consumer_key, consumer_secret, access_token, access_token_secret


# listener
class StdOutListener(StreamListener):
    
    def on_data(self, data):
        if not os.path.isfile(os.path.join(os.getcwd(), 'ravens_coords.csv')):
            c = open('ravens_coords.csv', 'w')
            c.write('long, lat\n')
            c.close()

        if not os.path.isfile(os.path.join(os.getcwd(), 'ravens_tweets.csv')):
            c = open('ravens_tweets.csv', 'w')
            c.write('tweet, time\n')
            c.close()

        t = open('ravens_tweets.csv', 'a+')
        c = open('ravens_coords.csv', 'a+')

        # serialize the output
        json_data = json.loads(data)

        # push the tweet text to the display
        # encode to utf-8 to avoid codec errors on Ubuntu
        timestamp = dt.datetime.fromtimestamp(int(json_data['timestamp_ms'])/1000)
        this_tweet = str(json_data['text'].encode('utf-8'))

        print('Tweet at {0}:\n{1}'.format(timestamp, this_tweet))
        print json_data['text'].encode('utf-8')
        t.write('"{0}", {1}\n'.format(this_tweet, timestamp))

        print str(json_data['coordinates']) + '\n'
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
    time.sleep(86400)
    stream.disconnect()

    end_time = time.strftime('%Y-%m-%d %H:%M:%S')

    print('Program start: {0:>3}'.format(start_time))
    print('Program finish: {0:>2}'.format(end_time))