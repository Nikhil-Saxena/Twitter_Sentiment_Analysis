import json

tweetsData = open('tweetsSentiment.json','r')
positiveTweetsFile = open('positiveTweets.json','w')
negativeTweetsFile = open('negativeTweets.json','w')
ignoreTweetsFile = open('ignoredTweets.json','w')
tweetsList = list(tweetsData)

for line in tweetsList:
    tweet = json.loads(line)
    if tweet['sentiment'] == 'p':
        json.dump(tweet, positiveTweetsFile)
        positiveTweetsFile.write('\n')
    elif tweet['sentiment'] == 'n':
        json.dump(tweet, negativeTweetsFile)
        negativeTweetsFile.write('\n')
    elif tweet['sentiment'] == 'i':
        json.dump(tweet, ignoreTweetsFile)
        ignoreTweetsFile.write('\n')

positiveTweetsFile.close()
negativeTweetsFile.close()
ignoreTweetsFile.close()
tweetsData.close()
