import simplejson as json
import urllib
import datetime
from datetime import timedelta
import oauth2

#folder and file details
keyFldr='twitterAcKeys'
keyFn='keys.txt'
twitterDataFldr='twitterData'
twitterDataJsonFn='tweetsForAllCompany.json'
companyAbvFldr='companyAbbvs'
companyAbvFn='companyAbbvs.txt'

#provide the date 
fromDateDataToFetch='2018-11-15'
tillDateDataToFetch='2018-11-09'
# Mention the number of days before the above given date tweeter data need to be downloaded


#From file read all the abbreviations of company names
finCmp=open(companyAbvFldr+'/'+companyAbvFn,'r')
companyAbbv=finCmp.read().split('\n')
finCmp.close()

#collect authentication keys from a file
finK=open(keyFldr+'/'+keyFn,'r')
keysAll=finK.read().split('\n')
finK.close()
keys={}
for ln in keysAll:
    a,b=ln.split('=')
    keys[a]=b


#function to collect twitter data, takes keyword as company name, given date and time duration
def obtainTwitterData(keyword,fromDateDataToFetch,tillDateDataToFetch):
    fromDate= datetime.datetime.strptime(fromDateDataToFetch,'%Y-%m-%d')
    tillDate=datetime.datetime.strptime(tillDateDataToFetch,'%Y-%m-%d')
    duration=fromDate-tillDate
    howLong = []
    howLong.append(fromDate.strftime("%Y-%m-%d"))
    for i in range(1,duration.days+1):
        dateDiff = timedelta(days=-i)
        newDate = fromDate + dateDiff
        howLong.append(newDate.strftime("%Y-%m-%d"))
    tweetsForDuration = {}

    for i in range(0,duration.days):
        startEndDate = {'since': howLong[i+1], 'until': howLong[i]}
        #collect tweets between given dates
        tweetsForDuration[i] = getDataBwDates(keyword, startEndDate)        
        print(tweetsForDuration[i])
    return tweetsForDuration

#prepare a query to search in api.twitter.com and fetch the data from api
def getDataBwDates(keyword, startEndDate = {}):
    maximumTweets = 10
    url = 'https://api.twitter.com/1.1/search/tweets.json?'
    query = {'q': keyword, 'lang': 'en', 'result_type': 'mixed', 'since_id': 2014,'count': maximumTweets, 'include_entities': 0}
    #add dates since and until
    if startEndDate:
        for key, value in startEndDate.items():
            query[key] = value

    #perform query on the twietter
    url += urllib.parse.urlencode(query)
    response,content = twitterAuthentication(url,keys)

    jsonUrlCont = json.loads(content)
    textTweets = []
    if 'errors' in jsonUrlCont:
        print ("Error while search query API")
        print (jsonUrlCont['errors'])
    else:
        for item in jsonUrlCont['statuses']:
            d = datetime.datetime.strptime(item['created_at'], '%a %b %d %H:%M:%S +0000 %Y')
            str = d.strftime('%Y-%m-%d')+" | "+item['text'].replace('\n', ' ')
            textTweets.append(str)
    return textTweets

#Twitter authentication using keys and fetch the data
def twitterAuthentication(url,keys,http_method="GET", post_body=None,http_headers=None):  
  consumer = oauth2.Consumer(key=keys['consumerKey'], secret=keys['consumerSecret'])
  token = oauth2.Token(key=keys['tokenKey'], secret=keys['tokenSecret'])
  client = oauth2.Client(consumer, token)
  response, content = client.request(url, method=http_method, body=bytes('', "utf-8"), headers=http_headers)
  return response,content

#A dictonary to collect all the data by twitter
allCompanyTweets ={}
for ci in range(len(companyAbbv)):
    companyAbbv_toSrch = '$'+companyAbbv[ci]    
    tweetsForACompany = obtainTwitterData(companyAbbv_toSrch,fromDateDataToFetch,tillDateDataToFetch)
    allCompanyTweets[companyAbbv[ci]]=tweetsForACompany
    print ("Tweets for the company "+companyAbbv_toSrch+" are fetched\n")

#print the collected tweets for companies
for ci in range(len(companyAbbv)):
    print("Tweets for company "+companyAbbv[ci])
    for tin in range(len(allCompanyTweets[companyAbbv[ci]])):
        print(allCompanyTweets[companyAbbv[ci]][tin])

#write the tweets for all companies into a json file
with open(twitterDataFldr+'/'+twitterDataJsonFn,'w') as f:
    json.dump(allCompanyTweets,f)
f.close()


fromDate= datetime.datetime.strptime(fromDateDataToFetch,'%Y-%m-%d')
tillDate=datetime.datetime.strptime(tillDateDataToFetch,'%Y-%m-%d')
duration=fromDate-tillDate
howLong = []
howLong.append(fromDate.strftime("%Y-%m-%d"))
for i in range(1,duration.days+1):
    dateDiff = timedelta(days=-i)
    newDate = fromDate + dateDiff
    howLong.append(newDate.strftime("%Y-%m-%d"))