import json
import random

tweetsData = {}
tweetsFile = open('tweetsSalman.txt','r')
ftw = open('tweetsSentiment.json','w')
tweetsList = list(tweetsFile)

count = 0
while count<25:
    index = random.randrange(0,len(tweetsList),2)
    try:
        tweet = json.loads(tweetsList[index])
        print tweet['text'] + '\n'
        i = input('tweet sentiment?')
        tweetsData['text']=tweet['text']
        tweetsData['sentiment']= i
        tweetsList.pop(index)
        if i != 'q':
            json.dump(tweetsData,ftw)
            ftw.write('\n')
            count += 1
    except:
        continue

ftw.close()
tweetsFile.close()
