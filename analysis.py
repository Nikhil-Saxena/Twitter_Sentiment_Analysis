import json
import nltk
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
import random
import re
import matplotlib.pyplot as plt

stop = stopwords.words('english')
stemmer = SnowballStemmer("english", ignore_stopwords=True)
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
        tweet['text'] = applyStemmerToTweet(tweet['text'])
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

def classifier(noOfFeatures):
    allWords = []
    for (words,sentiment) in trainingTweetsWords:
        allWords.extend(words)
    wordList = nltk.FreqDist(allWords)
    wordList = sorted(wordList.iteritems(),key=lambda(k,v):(v,k),reverse=True)
    wordList = [word for (word,freq) in wordList]
    #print wordList[:10]
    #print set(wordList)
    #wordList = set(wordList) - set(stop)
    #wordList = list(wordList)
    #print len(wordList)
    #print wordList[:10]
    for word in wordList:
        if word in stop:
            wordList.remove(word)
        elif re.search(r'http[\w:]+',word):
            wordList.remove(word)
        elif re.search(r'[\w:?]*@\w*',word):
            wordList.remove(word)
        elif re.search(r'\\u[\w:@.]*',word):
            wordList.remove(word)          
            
    #print len(wordList)
    return wordList[:noOfFeatures]

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

def applyStemmerToTweets(tweets):
    stemmedTweets = []
    for tweet in tweets:
        stemmedTweets.append(applyStemmerToTweet(tweet))
    return stemmedTweets

def applyStemmerToTweet(tweet):
    return ' '.join([stemmer.stem(word) for word in tweet.split()])

def main():
    initializeLists()
    i=10
    seperateTestTraining(i)
    extract_words(trainingTweetsWords, trainingTweets)
    noOfFeatures = 91    
    wordFeatures.extend(classifier(noOfFeatures))
    trainingSet = nltk.classify.apply_features(extract_features, trainingTweetsWords)
    Classifier = nltk.NaiveBayesClassifier.train(trainingSet)
    #checking accuracy
    count = 0
    for (tweet,sentiment) in testTweets:
        prediction = Classifier.classify(extract_features(tweet.split()))
        if prediction == sentiment:
            count += 1
    accuracy = count/float(len(testTweets))
    print 'accuracy using %d*3 trainingTweets = '%i + str(accuracy)
    sampleTweet  = 'accha hua warna paise se wishwaas uth jaata'
    sampleTweet = applyStemmerToTweet(sampleTweet)
    print 'sample prediction: ' + Classifier.classify(extract_features(sampleTweet.split()))

if __name__ == '__main__':
    main()
