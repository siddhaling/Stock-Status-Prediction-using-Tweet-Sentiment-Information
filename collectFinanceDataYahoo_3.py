import datetime
import time
from urllib.request import urlopen
from bs4 import BeautifulSoup as bs
import simplejson as json

#folder and file details
companyAbvFldr='companyAbbvs'
companyAbvFn='companyAbbvs.txt'
financeDataFldr='yahooFinData'
stockPrzOpenFn='stockPriceOpenAllCompany.json'
stockPrzCloseFn='stockPriceCloseAllCompany.json'

#Specify the from date to previous till date. Between this two dates data is fetched
fromDateDataToFetch='2018-11-15'
tillDateDataToFetch='2018-11-09'

#collect finance trend history from finance.yahoo.com
def trendHistoryFromYahoo(name,eDate,sDate):
    trendHistory = []
    startDateNumeric=time.mktime(datetime.datetime.strptime(sDate, '%Y-%m-%d').timetuple())
    startDateNumeric=str(int(startDateNumeric))
    endDateNumeric=time.mktime(datetime.datetime.strptime(eDate, '%Y-%m-%d').timetuple())
#    endDateNumeric+=datetime.timedelta(days=1)
    endDateNumeric=str(int(endDateNumeric))

    url="https://finance.yahoo.com/quote/"+name+"/history?period1="+startDateNumeric+"&period2="+endDateNumeric+"&interval=1d&filter=history&frequency=1d"
    dataFetchdYahoo=urlopen(url).read()
    gatherRows = bs(dataFetchdYahoo).findAll('table')[0].tbody.findAll('tr')

    for each_row in gatherRows:
        divisions = each_row.findAll('td')        
        if divisions[1].span.text  != 'Dividend': 
            #I'm only interested in 'Open' price; For other values, play with divs[1 - 5]
            trendHistory.append({'Date': divisions[0].span.text, 'Open': float(divisions[1].span.text.replace(',','')),'High':float(divisions[2].span.text.replace(',','')),'Low':float(divisions[3].span.text.replace(',','')),'Close':float(divisions [4].span.text.replace(',','')),'AdjClose':float(divisions[5].span.text.replace(',','')),'Volume':float(divisions[6].span.text.replace(',',''))})

    return trendHistory


#A text file contain all the company abbrevations
finCmp=open(companyAbvFldr+'/'+companyAbvFn,'r')
companyAbbv=finCmp.read().split('\n')
finCmp.close()

stockPriceOpenAllCpmy={}
stockPricesCloseAllCpmy={}
#for each company collect trend history
for ci in range(len(companyAbbv)):
    if not companyAbbv[ci]:
        continue
    print ('Collecting yahoo finance data for:'+companyAbbv[ci])    
    trendHistory = trendHistoryFromYahoo(companyAbbv[ci],fromDateDataToFetch,tillDateDataToFetch)     
    stockPriceOpen= {}
    stockPriceClose= {}
    highestPrice= {}
    lowestPrice = {}
    for i in range(len(trendHistory)):
        date = trendHistory[i]['Date'].replace(",","")
        stockPriceOpen.update({date: trendHistory[i]['Open']})
        stockPriceClose.update({date: trendHistory[i]['Close']})
        highestPrice.update({date: trendHistory[i]['High']})
        lowestPrice.update({date: trendHistory[i]['Low']})

    stockPriceOpenAllCpmy[companyAbbv[ci]]=stockPriceOpen
    stockPricesCloseAllCpmy[companyAbbv[ci]]=stockPriceClose


#write in JSON file format
with open(financeDataFldr+'/'+stockPrzOpenFn,'w') as f:
    json.dump(stockPriceOpenAllCpmy,f)

with open(financeDataFldr+'/'+stockPrzCloseFn,'w') as f:
    json.dump(stockPricesCloseAllCpmy,f)