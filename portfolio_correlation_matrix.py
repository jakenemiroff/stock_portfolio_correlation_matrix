import numpy as np
import requests
import pandas as pd
import pandas_datareader.data as web
import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
import mplfinance as mpf
import matplotlib.dates as mdates
import os

style.use('ggplot')

startDate = dt.datetime(2020, 1, 1)
endDate = dt.datetime(2020, 10, 15)

MY_STOCKS = ['AAPL', 'CHKP', 'CLOU',
            'ILMN', 'JNJ', 'KXS.TO', 'MSFT', 'PG',
            'SNPS', 'SPLK', 'SQ', 'TSM', 'VGK', 'VGT',
            'VTV', 'WIX', 'AMZN', 'COST', 'HD', 'IEMG',
            'RY', 'TCEHY', 'TOU.TO', 'WM', 'XBI']

def getYahooData():

    if not os.path.exists('stocksData'):

        os.makedirs('stocksData')

    for ticker in MY_STOCKS:

        if not os.path.exists('stocksData/{}.csv'.format(ticker)):

            df = web.DataReader(ticker, 'yahoo', startDate, endDate)
            df.reset_index(inplace=True)
            df.set_index("Date", inplace=True)
            df.to_csv('stocksData/{}.csv'.format(ticker))

getYahooData()

def buildDataFrame():

    mainDF = pd.DataFrame()

    for numberOfStocks, ticker in enumerate(MY_STOCKS):

        df = pd.read_csv('stocksData/{}.csv'.format(ticker))
        df.set_index('Date', inplace = True)
        df.drop(['Open', 'High', 'Low', 'Close', 'Volume'], 1, inplace = True)
        df.rename(columns = {'Adj Close' : ticker}, inplace = True)

        if mainDF.empty:

            mainDF = df

        else:

            mainDF = mainDF.join(df, how = 'outer')

    mainDF.to_csv('MY_STOCKS_joined_closes.csv')

buildDataFrame()
