import numpy as np
import pandas as pd
import talib #技術指標套件
import yfinance as yf #股價下載套件
from datetime import datetime
from pandas_datareader import data #資料讀取套件
import pandas as pd
import matplotlib.pyplot as plt #畫圖套件
import statistics #統計函數套件
import os

def drawStockSeries(df, xLabel):
    df[['close']].plot(figsize=(12,5))
    plt.title(xLabel, size=15)
    plt.legend(loc = "best", fontsize=12)
    plt.show()


yf.pdr_override()
target_stock = '2330.tw' #分析公司代號 e.g., '2330.TW'是台積電
start_date = datetime(2021, 1, 1) #設定資料開始日期
end_date = datetime(2021, 6, 30) #設定資料結束日期

#將資料放到Dataframe裡面
df = data.get_data_yahoo([target_stock], start_date, end_date)

#保留所需欄位
df = df.reindex(columns = ['Open','High', 'Low', 'Close', 'Volume'])
df.rename(columns={'Open':'open', 'High':'high', 'Low':'low', 'Close':'close',
                    'Volume':'volume' }, inplace = True) #更改欄位名稱
#畫出股價序列圖
print(df)

#將df與target_stockt傳入函數，畫出股價序列圖
drawStockSeries(df, target_stock)



close_sma_5 = np.round(talib.SMA(df['close'], timeperiod=5), 2)
close_sma_10 = np.round(talib.SMA(df['close'], timeperiod=10), 2)
close_sma_20 = np.round(talib.SMA(df['close'], timeperiod=20), 2)
indexDate = df.index
xpt = indexDate
ypt1 = close_sma_5
ypt2 = close_sma_10
ypt3 = close_sma_20
print(close_sma_5)
print(close_sma_10)
print(close_sma_20)

def drawMA5_10_20Series(xValues, yValues1, yValues2, yValues3, target_stock):
    plt.figure(figsize=(12,5))
    plt.title(target_stock, size=15)
    plt.plot(xValues,yValues1,'-', color = 'r', label="MA-5") #畫線
    plt.plot(xValues,yValues2,'+', color = 'g', label="MA-10") #畫線
    plt.plot(xValues,yValues3,'x', color = 'b', label="MA-20") #畫線
    plt.legend(loc = "best", fontsize=12)
    plt.show() #顯示繪製的圖形

#利用matplotlib畫出移動平均線
drawMA5_10_20Series(xpt, close_sma_5, close_sma_10, close_sma_20, target_stock)

