from twython import TwythonStreamer, TwythonError, Twython
import json

APP_KEY = '3vojitMRV06dWGdMJDb1eWKI9'
APP_SECRET = 'fGhxVat5cXvro3IzEHyjauduNQpnO26FwD4hKSZwQ64ucnm9SJ'
OAUTH_TOKEN  = '41348505-3eby6GPwQMSkL1Lz2sXVYIKUrf2P2K2gvlabjc9Yr'
OAUTH_TOKEN_SECRET = '8kTWNymhcvmC5HDFphwiZgOH1j0ctVoW8GHbfXsFLCqeH'

twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
t = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
coords = []

results = twitter.cursor(t.search, q='twitter', lang='eng')

i=0
for result in results:
    if result['coordinates'] is not None:
        coords.append(result['coordinates'])
        print(result['coordinates'])
    else:
        print('next')
        results.next()
    i += 1

print(coords)

# try:
#     for result in results['id_str']['statuses']:
#         if tweet['coordinates'] is not None:
#             coords.append(tweet['coordinates'])
# except TwythonError as e:
#     print(e)

# print(coords)

# try:
#     results = twitter.cursor(t.search, q='steelers', lang='en')
#     for result in results: print(result)
# except TwythonError as e:
#     print(e)
# print('results length: {0}'.format(len(results)))
# print json.dumps(results)
# try:
#     for tweet in results['statuses']:
#         if tweet['coordinates'] is not None:
#             coords.append(tweet['coordinates'])
# except TwythonError as e:
#     print(e)

# while len(results) != 0:
#     try:
#         results = twitter.search(q='steelers', lang='en', count=100,
#                                  max_id=results[len(results)-1]['id']-1)
#     except TwythonError as e:
#         print(e)
#     for tweet in results:
#         coords.append(tweet['coordinates'])

# print(coords)


#     '''
# Get all tweets from a given user.
# Batch size of 200 is the max for user_timeline.
# '''
# from twython import Twython, TwythonError
# tweets = []
# # Requires Authentication as of Twitter API v1.1
# twitter = Twython(PUT YOUR TWITTER KEYS HERE!)
# try:
#     user_timeline = twitter.get_user_timeline(screen_name='eugenebann',count=200)
# except TwythonError as e:
#     print e
# print len(user_timeline)
# for tweet in user_timeline:
#     # Add whatever you want from the tweet, here we just add the text
#     tweets.append(tweet['text'])
# # Count could be less than 200, see:
# # https://dev.twitter.com/discussions/7513
# while len(user_timeline) != 0: 
#     try:
#         user_timeline = twitter.get_user_timeline(screen_name='eugenebann',count=200,max_id=user_timeline[len(user_timeline)-1]['id']-1)
#     except TwythonError as e:
#         print e
#     print len(user_timeline)
#     for tweet in user_timeline:
#         # Add whatever you want from the tweet, here we just add the text
#         tweets.append(tweet['text'])
# # Number of tweets the user has made
# print len(tweets)