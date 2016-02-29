import json
f = open('testwrite.txt','r')
l = list(f)

for tweet in l:
    try:
        t = json.loads(tweet)
        print type(tweet), type(t)
    except:
        continue
