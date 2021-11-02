# -*- coding: utf-8 -*-

# -- Sheet --



import requests
import sys
import time
import csv
import pandas
import json
import os.path


# using v6/finance/quote API call
url = "https://yfapi.net/v6/finance/quote"

# getting stock ticker from command line argument
stock_ticker = str(sys.argv[1])
querystring = {"symbols":stock_ticker}

# personal API key
headers = {
    'x-api-key': "VYY2kx4kCg80jTu3jXSP47x8izo61aM2Ea05FfVg"
    }

response = requests.request("GET", url, headers=headers, params=querystring)

# handling different response status codes
response.raise_for_status()
# stock data in json format
stock_data = response.json()
if stock_data['quoteResponse']['result']== []:
    # means Client Error, as per quiz - right now erroneus errors 
    # only mean entered incorrect stock ticker
    sys.exit('Erroneus Input. Client Error. You entered Stock Ticker: ' + stock_ticker +
        '. This is not a known Stock Ticker. Please try again.')
    

# converting market time to human readable number format
market_time = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(stock_data['quoteResponse']['result'][0]['regularMarketTime']))

# printing to command line in desired format
print('Current Price: ' + str(stock_data['quoteResponse']['result'][0]['regularMarketPrice']) + '\n'
    + 'Market Time: ' + market_time + '\n'
    + 'Company Name: ' + str(stock_data['quoteResponse']['result'][0]['displayName']))

# Stock Ticker, Market Time, Price
row_to_write = [[stock_ticker,market_time,stock_data['quoteResponse']['result'][0]['regularMarketPrice']]]
row_df = pandas.DataFrame(row_to_write)
# writing to csv with desired headers
# see if file is empty - if it is, write header

# open the file
f = open('Quiz2_StockAPI.csv','a')
fileEmpty = os.stat('Quiz2_StockAPI.csv').st_size == 0
if fileEmpty:
    row_df.to_csv('Quiz2_StockAPI.csv', mode='a', header=['Ticker', 'Market Time', 'Price'])
else:
    row_df.to_csv('Quiz2_StockAPI.csv', mode='a', header=False)

