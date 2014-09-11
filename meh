from twython import TwythonStreamer, TwythonError, Twython

APP_KEY = 'secret'
APP_SECRET = 'secret'
OAUTH_TOKEN  = 'I\'ve got a'
OAUTH_TOKEN_SECRET = 'secret'

twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

i=0
while i <= 9:
    print(i)
    results = twitter.search(q='steelers', lang='en')
    try:
        for tweet in results['statuses']:
            if tweet['coordinates'] is not None:
                print(tweet['coordinates'])
    except TwythonError as e:
        print(e)

    i += 1