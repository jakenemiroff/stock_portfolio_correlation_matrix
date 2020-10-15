import numpy as np
import requests
import pandas as pd
import pandas_datareader.data as web
import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style

style.use('ggplot')

startDate = dt.datetime(2020, 1, 1)
endDate = dt.datetime(2020, 10, 15)

df = web.DataReader('AAPL', 'yahoo', startDate, endDate)

# df.to_csv('AAPL.csv')

# df = pd.read_csv('AAPL.csv', parse_dates = True, index_col = 0)

# print(df.head())
