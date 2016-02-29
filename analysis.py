import json
import nltk
from nltk.corpus import stopwords
import random

stop = stopwords.words('english')
positiveTweets = []
negativeTweets = []
ignoreTweets = []
trainingTweets = []
testTweets = []
trainingTweetsWords = []
wordFeatures = []

def initializeLists():
    tweetsData = open('tweetsSentiment.json','r')
    tweetsList = list(tweetsData)
    for line in tweetsList:
        tweet = json.loads(line)
        if tweet['sentiment'] == 'p':
            positiveTweets.append((tweet['text'],tweet['sentiment']))
        elif tweet['sentiment'] == 'n':
            negativeTweets.append((tweet['text'],tweet['sentiment']))
        elif tweet['sentiment'] == 'i':
            ignoreTweets.append((tweet['text'],tweet['sentiment']))
    tweetsData.close()

def extract_words(appendTo,fromTweets):
    for (words,sentiment) in fromTweets:
        words_filtered = [word.lower() for word in words.split() if len(word)>2]
        appendTo.append((words_filtered, sentiment))

def classifier():
    allWords = []
    for (words,sentiment) in trainingTweetsWords:
        allWords.extend(words)
    #wordList = nltk.FreqDist(allWords)
    #print sorted(wordList.iteritems(),key=lambda(k,v):(v,k),reverse=True)
    #remove= ['and','the','have','has','@nav_prdp:', ]
    wordList = set(allWords) - set(stop)
    wordList = list(wordList)
    #print len(wordList)
    #print wordList
    for word in wordList:
        if 'http' in word:
            wordList.remove(word)
        if '@' in word:
            wordList.remove(word)
        if '\u' in word:
            wordList.remove(word)
    #print len(wordList)
    return wordList

def extract_features(tweetWords):
    tweetWords = set(tweetWords)
    features = {}
    for word in wordFeatures:
        features['contains(%s)' %word] = (word in tweetWords)
    return features

def seperateTestTraining(i):
    count = 0
    while count<=i:
        index = random.randrange(len(positiveTweets))
        trainingTweets.append(positiveTweets[index])
        positiveTweets.pop(index)
        count += 1
    count = 0
    while count<=i:
        index = random.randrange(len(negativeTweets))
        trainingTweets.append(negativeTweets[index])
        negativeTweets.pop(index)
        count += 1
    count = 0
    while count<=i:
        index = random.randrange(len(ignoreTweets))
        trainingTweets.append(ignoreTweets[index])
        ignoreTweets.pop(index)
        count += 1
    testTweets.extend(positiveTweets+negativeTweets+ignoreTweets)


def main():
    initializeLists()
    i=10
    seperateTestTraining(i)
    print len(trainingTweets)
    print len(testTweets)
    #trainingTweets.extend(positiveTweets[:i] + negativeTweets[:i] + ignoreTweets[:i])
    #testTweets.extend(positiveTweets[i:] + negativeTweets[i:] + ignoreTweets[i:])
    extract_words(trainingTweetsWords, trainingTweets)
    wordFeatures.extend(classifier())
    trainingSet = nltk.classify.apply_features(extract_features, trainingTweetsWords)
    Classifier = nltk.NaiveBayesClassifier.train(trainingSet)
    #print Classifier.show_most_informative_features(32)
    #checking accuracy
    count = 0
    for (tweet,sentiment) in testTweets:
        prediction = Classifier.classify(extract_features(tweet.split()))
        #print prediction,sentiment
        if prediction == sentiment:
            count += 1
    #print count
    print 'accuracy %d = '%i + str(count/float(len(testTweets)))
    sampleTweet  = 'accha hua warna paise se wishwaas uth jaata'
    print 'sample prediction: ' + Classifier.classify(extract_features(sampleTweet.split()))

if __name__ == '__main__':
    main()
