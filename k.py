
from twython import Twython
twitter = Twython()
# Displaying the Daily Trends.
trends = twitter.getDailyTrends()
print(trends)
