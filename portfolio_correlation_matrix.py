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
            print(df.head())
            df.reset_index(inplace=True)
            df.set_index("Date", inplace=True)
            df.to_csv('stocksData/{}.csv'.format(ticker))

getYahooData()
