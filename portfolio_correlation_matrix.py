from questrade_api import Questrade
import numpy as np
import pandas as pd
import pandas_datareader.data as web
import datetime as dt
import seaborn as sns
import matplotlib.pyplot as plt
import os
from calendar import isleap

def subtract_years(d, years):
    new_year = d.year - years
    try:
        return d.replace(year=new_year)
    except ValueError:
        if (d.month == 2 and d.day == 29 and # leap day
            isleap(d.year) and not isleap(new_year)):
            return d.replace(year=new_year, day=28)
        raise

endDate = dt.datetime.today()
startDate = subtract_years(endDate, 5)

ETFs = ['VGT', 'VGK', 'XBI', 'IZRL', 'CLOU', 'XBI', 'VOO', 'IEMG', 'BUG']

prospectiveStocks = {'AMAT':0, 'SHOP':0}

def getAccountNumbers(q):

    accounts = []

    for account in q.accounts['accounts']:
        accounts.append((account['type'], account['number']))

    return accounts

def getPortfolioTotalEquity(q, accounts):

    marketValue = 0

    for account in accounts:
        for balance in q.account_balances(account[1])['sodCombinedBalances']:
            
            if balance['currency'] == 'USD':
                pass
            else:
                marketValue += balance['totalEquity']

    return round(marketValue, 2)

def getAccountHoldings(q, accounts):

    holdings = dict()

    for account in accounts:
        for position in q.account_positions(account[1])['positions']:
            if position['symbol'] == 'BRK.B':
                holdings['BRK-B'] = position['currentMarketValue']
            elif position['symbol'] in ETFs:
                pass
            else:
                if position['symbol'] in holdings:
                    holdings[position['symbol']] += position['currentMarketValue']

                else:
                    holdings[position['symbol']] = position['currentMarketValue']

    holdings = holdings | prospectiveStocks
    return holdings

def getYahooData(holdings):

    listOfStocks = list(holdings.keys())

    if not os.path.exists('stocksData'):

        os.makedirs('stocksData')

    for ticker in listOfStocks:

        if not os.path.exists('stocksData/{}.csv'.format(ticker)):

            # test = web.get_data_yahoo(ticker, startDate, endDate)
            # df = web.DataReader(ticker, 'yahoo', startDate, endDate)
            df = web.get_data_yahoo(ticker, startDate, endDate, interval='m')

            df.reset_index(inplace=True)
            df.set_index("Date", inplace=True)
            df['Returns'] = df['Adj Close'].pct_change()
            df.to_csv('stocksData/{}.csv'.format(ticker))

def buildDataFrame(holdings, totalEquity):

    listOfStocks = list(holdings.keys())
    mainDF = pd.DataFrame()

    for numberOfStocks, ticker in enumerate(listOfStocks):

        df = pd.read_csv('stocksData/{}.csv'.format(ticker))
        df.set_index('Date', inplace = True)
        df.drop(['Open', 'High', 'Low', 'Close', 'Volume', 'Adj Close'], 1, inplace = True)
        df.rename(columns = {'Returns' : ticker + ' ' + str(round((holdings[ticker] / totalEquity * 100), 2)) + '%'}, inplace = True)
        
        if mainDF.empty:
            mainDF = df

        else:
            mainDF = mainDF.join(df, how = 'outer')

    mainDF.to_csv('MY_STOCKS_joined_closes.csv')

def visualizeData():

    df = pd.read_csv('MY_STOCKS_joined_closes.csv')

    correlation = df.corr()

    plt.figure(figsize=(16, 8))

    ax = sns.heatmap(correlation, annot = True, vmin=-1, vmax=1, center= 0, cmap= 'coolwarm', linewidths=0.5, linecolor='black')

    plt.show()

def main():

    # q = Questrade(refresh_token='F6RwoQL4chny8F_ZGutons5a-kr8cYJx0')
    q = Questrade()

    accounts = getAccountNumbers(q)
    # print(accounts)

    totalEquity = getPortfolioTotalEquity(q, accounts)
    # print(totalEquity)

    holdings = getAccountHoldings(q, accounts)
    # print(holdings)

    getYahooData(holdings)
    buildDataFrame(holdings, totalEquity)
    visualizeData()

main()
