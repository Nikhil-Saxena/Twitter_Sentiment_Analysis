import tweepy
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

# Consumer keys and access tokens, used for OAuth
consumer_key = 'yourKey'
consumer_secret = 'yourSecret'
access_token = 'yourToken'
access_token_secret = 'yourTokenSecret'

class StdOutListener(StreamListener):
    ''' Handles data received from the stream. '''

    def on_data(self, data):
        print data
        return True

    def on_error(self, status):
        print status

if __name__ == '__main__':
    listener = StdOutListener()
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    stream = Stream(auth, listener)
    stream.filter(track=['salman','salman verdict','hit and run','#beinghuman','bhai','#bhai'])
