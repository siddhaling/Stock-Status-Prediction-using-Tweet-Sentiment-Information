import datetime
import numpy as np
import csv
import simplejson as json

#folder and file details
featuresFldr='twFeaturesAndCls'
financeDataFldr='yahooFinData'
twitterDataFldr='twitterData'
featuresFn="stockpredict.txt"
tweetSentiScrFn='tweetsSentiScoreAndCls.csv'
stockPrzOpenFn='stockPriceOpenAllCompany.json'
stockPrzCloseFn='stockPriceCloseAllCompany.json'

#open a file for writing the features and class information
file = open(featuresFldr+'/'+featuresFn, "w",encoding="utf-8")
#read the stock open prices from json file
with open(financeDataFldr+'/'+stockPrzOpenFn,'r') as f:
    stockPriceOpenAllCompany=json.load(f)
#read the stock close prices from json file
with open(financeDataFldr+'/'+stockPrzCloseFn,'r') as ff:
    stockPriceCloseAllCompany=json.load(ff)

#open csv file containing tweets
fileRCSV=open(twitterDataFldr+'/'+tweetSentiScrFn, 'r',encoding='utf=8')
#read all tweets from CSV file to a list
inpAllTweets = csv.reader(fileRCSV, delimiter=',')
inpAllTweets=list(inpAllTweets)

#Collect all tweets related to a company and date of tweet in lists
def collectCompTweetsAndDates(companyAbb,inpAllTweets):
    compTweetsOnDate =[]
    compTweets= []
    for row in inpAllTweets:
        if len(row) == 5 and row[0] == companyAbb:            
            compTweets.append(row)
            print(row[0],companyAbb,row)
            date = row[2]
            compTweetsOnDate.append(date)
    return compTweets,compTweetsOnDate

#Count the number of positve, negative and neutral for a company
def getDatewiseSentiDetail(aDate,compTweets):
    dateTotalCount = 0
    datePosCount = 0
    dateNegCount = 0
    dateNutCount = 0
    totalSentimentScore = 0.
    for row in compTweets:
        sentiment = row[1]
        temp_date = row[2]
        sentiment_score = row[4]
        if(temp_date == aDate):
            totalSentimentScore += float(sentiment_score)
            dateTotalCount+=1
            if (sentiment == 'positive'):
                datePosCount+=1
            elif (sentiment == 'negative'):
                dateNegCount+=1
            elif (sentiment == 'neutral'):
                dateNutCount+=1    
    s = str(dateTotalCount)+" "+str(datePosCount)+" "+str(dateNegCount)+" "+str(dateNutCount)
    return s,dateTotalCount,datePosCount, dateNegCount, dateNutCount

#obtain openning an closing price of a stock. 
def getStockPriceDetails(aDate,company_open_price,company_close_price):
    aDate = aDate.strip()
    day = datetime.datetime.strptime(aDate, '%Y-%m-%d').strftime('%A')
    closingPrice = 0.
    openingPrice = 0.
    if day == 'Saturday':
        aDateParticulars = aDate.split("-")
        if len(str((int(aDateParticulars[2])-1)))==1:
            aDate = aDateParticulars[0]+"-"+aDateParticulars[1]+"-0"+str((int(aDateParticulars[2])-1))
        else:
            aDate = aDateParticulars[0] + "-" + aDateParticulars[1] + "-" + str((int(aDateParticulars[2]) - 1))
        dateInMonthDayYr=datetime.datetime.strptime(aDate,'%Y-%m-%d')
        dateInMonthDayYr=dateInMonthDayYr.strftime("%b %d %Y")
        openingPrice = company_open_price[dateInMonthDayYr]
        closingPrice = company_close_price[dateInMonthDayYr]
    elif day == 'Sunday':
        aDateParticulars = aDate.split("-")
        if len(str((int(aDateParticulars[2])-2)))==1:
            aDate = aDateParticulars[0]+"-"+aDateParticulars[1]+"-0"+str((int(aDateParticulars[2])-2))
        else:
            aDate = aDateParticulars[0] + "-" + aDateParticulars[1] + "-" + str((int(aDateParticulars[2]) - 2))
        dateInMonthDayYr=datetime.datetime.strptime(aDate,'%Y-%m-%d')
        dateInMonthDayYr=dateInMonthDayYr.strftime("%b %d %Y")
        openingPrice = company_open_price[dateInMonthDayYr]
        closingPrice = company_close_price[dateInMonthDayYr]
    else:
        dateInMonthDayYr=datetime.datetime.strptime(aDate,'%Y-%m-%d')
        dateInMonthDayYr=dateInMonthDayYr.strftime("%b %d %Y")
        openingPrice = company_open_price[dateInMonthDayYr]
        closingPrice = company_close_price[dateInMonthDayYr]

    return dateInMonthDayYr,dateInMonthDayYr,openingPrice,closingPrice

#for each compnay name find the opennin,closing prices and sentiment associated with tweets
for companyAbb in stockPriceOpenAllCompany.keys():
    company_open_price=stockPriceOpenAllCompany[companyAbb]
    company_close_price=stockPriceCloseAllCompany[companyAbb]
    print (companyAbb)

    compTweets,compTweetsOnDate=collectCompTweetsAndDates(companyAbb,inpAllTweets)
    datewiseSentiDetails = {}

    for aDate in np.unique(compTweetsOnDate):
        s,dateTotalCount,datePosCount,dateNegCount,dateNutCount=getDatewiseSentiDetail(aDate,compTweets)

        dateInMonthDayYr,dateInMonthDayYr,openingPrice,closingPrice=getStockPriceDetails(aDate,company_open_price,company_close_price)
        compMarketStatus = 0
        if (float(closingPrice)-float(openingPrice)) > 0:
            compMarketStatus = 1
        else:
            compMarketStatus =-1
        file.write( str(datePosCount) + "," + str(dateNegCount) + "," + str(dateNutCount) +"," + str(dateTotalCount) + "," + str(compMarketStatus) + "\n")

file.close()
fileRCSV.close()
print( "Dataset cotaining sentiment info and stock status is prepared.\n")