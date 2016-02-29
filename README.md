#**Twitter_Sentiment_Analysis**
	
######A naive bayes sentiment classifier coded in python. Classifies the tweets into 3 categories Positive, Negative and Neutral.
  - tweets related to salman khan hit and run case verdict are used as example
  - uses the NLTK stopword corpus and SnowballStemmer
  - tweets fetched using the tweepy python library
  - the accuracy may vary, since the training set is randomly choosen on each run

###Files: 

- analysis.py : The Director of the code. (main)
- assignSentiments.py : lists through the tweets and asks to classify the tweets for the training and test sets.
- getTweets.py : fetches the tweets having the track words from the twitter stream.
- sortSentimentFiles: list the sorted tweets into their respective sentiment files (not required, used for analysis only)
