import json
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import time
import re
import os

# search terms, ariana will get some tweets, reno not too many
search_terms = ['#nfl', 'goodell', 'nflcommish', '#RayRice']

# Twitter API credentials
consumer_key = 'secret'
consumer_secret = 'secret'
access_token = 'I\'ve got a'
access_token_secret = 'secret'

# listener
class StdOutListener(StreamListener):
    
    def on_data(self, data):
        if not os.path.isfile(os.path.join(os.getcwd(), 'nfl_coords.csv')):
            c = open('nfl_coords.csv', 'w')
            c.write('long, lat\n')
            c.close()

        t = open('nfl_tweets.csv', 'a+')
        c = open('nfl_coords.csv', 'a+')
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
        print status.encode('utf-8')

if __name__ == '__main__':
 
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)
    stream.filter(track=search_terms, async=True)
    time.sleep(18000)
    stream.disconnect()

    # f = open('coords.csv', 'w')
    # f.write('long, lat\n')
    # for location in coords:
    #     m = re.search('-[\d|., ]*', str(location))
    #     if m is not None:
    #         print(m.group())
    #         f.write(str(m.group()) + '\n')

    # f.close()

    # f = open('tweets.csv', 'w')
    # for tweet in tweets:
    #     if tweet is not None:
    #         f.write(str(tweet) + '\n')

    # f.close()


