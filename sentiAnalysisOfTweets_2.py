import simplejson as json
from urllib.request import urlopen
from zipfile import ZipFile
import io
import re

import csv

#folder and file details
twitterDataFldr='twitterData'
twitterDataJsonFn='tweetsForAllCompany.json'
twitterSentimentInfoFn='tweetsSentiScoreAndCls.csv'

#Function tokenizes the given text
def textTokenizer(input):
    return re.sub('\W+', ' ', input.lower()).split()

#function to find sentiment based on AFINN dictonary and return the total and score
def findAFINNSentiment(tokens, afinnDict):
    total = 0.0
    afinnScores=[]
    for t in tokens:
        if t in afinnDict:
            total += afinnDict[t]
            afinnScores.append(afinnDict[t])
    return total,afinnScores

#display tweets and corresponding sentiment values
def displayTweetAndSentiVals():
    for t in tweets:
        tokens=[textTokenizer(t)]
        afinnTotal = []
        for tweet in tokens:
            total,afinnScore = findAFINNSentiment(tweet, afinnDict)
            print (t,tweet,total,afinnScore)
            afinnTotal.append(total)

#function to convert AFINN file to dictonary
def AFINNtoDic(zipfileAFINN):
    afinnFile = zipfileAFINN.open('AFINN/AFINN-111.txt','r')
    afinn = dict()
    for line in afinnFile:
        line=line.decode()
        words = line.strip().split()
        if len(words) == 2:
            afinn[words[0]] = int(words[1])
    return afinn

# Obtain AFINN lexicon from url 
url = urlopen('http://www2.compute.dtu.dk/~faan/data/AFINN.zip')
zipfileAFINN = ZipFile(io.BytesIO(url.read()))
afinnDict=AFINNtoDic(zipfileAFINN)

with open(twitterDataFldr+'/'+twitterDataJsonFn,'r') as f:
    tweetsAllComapy=json.load(f)
f.close()

#Sentiment analysis of tweets
ftweetSentiCls = open(twitterDataFldr+'/'+twitterSentimentInfoFn, 'w', encoding="utf-8")
csvWriterTweetSentiCls = csv.writer(ftweetSentiCls)

#iterate through all company tweets and compute sentiment based on AFINN
for company in tweetsAllComapy.keys():
    print ("Sentiment calculation for...",company)
    tweets = []
    for itweets in tweetsAllComapy[company].keys():
        print (itweets,len(tweetsAllComapy[company][itweets]))
        tweets.extend(tweetsAllComapy[company][itweets])

    tokens = [textTokenizer(t) for t in tweets]  # Tokenizing tweets

    afinnScoreForAllToks = []
    
    for tOftweet in tokens:
        total,afinnScore = findAFINNSentiment(tOftweet , afinnDict)  
        afinnScoreForAllToks.append(total)
    
    positiveTweet = []
    negativeTweet = []
    neutralTweet = []
# Seperating Positive, negative and neutral tweets based on afinnScoreForAllToks
    for i in range(len(afinnScoreForAllToks)):
        if afinnScoreForAllToks[i] > 0:
            positiveTweet.append(afinnScoreForAllToks[i])
            csvWriterTweetSentiCls.writerow([company,"positive", str(tweets[i].split("|")[0]), str(tweets[i].split("|")[1]), float(afinnScoreForAllToks[i])])
        elif afinnScoreForAllToks[i] < 0:
            negativeTweet.append(afinnScoreForAllToks[i])
            csvWriterTweetSentiCls.writerow([company,"negative",  str(tweets[i].split("|")[0]), str(tweets[i].split("|")[1]),float(afinnScoreForAllToks[i])])
        else:
            neutralTweet.append(afinnScoreForAllToks[i])
            csvWriterTweetSentiCls.writerow([company,"neutral", str(tweets[i].split("|")[0]), str(tweets[i].split("|")[1]),float(afinnScoreForAllToks[i])])
    
ftweetSentiCls.close()
