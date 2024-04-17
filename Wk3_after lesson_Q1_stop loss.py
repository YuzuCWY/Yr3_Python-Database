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

target_stock = '2498.tw' #分析公司代號
start_date = datetime(2021, 1, 1) #設定資料開始日期
end_date = datetime(2021, 7, 19) #設定資料結束日期
stopLoss = 0.1



# Define RSI thresholds
rsi_buy_threshold = 30
rsi_sell_threshold = 70

# Set EMA thresholds for buy and sell signals
ema_buy_threshold = 5
ema_sell_threshold = 10




#將資料放到Dataframe裡面
df = data.get_data_yahoo([target_stock], start_date, end_date)

#保留所需欄位
df = df.reindex(columns = ['Open','High', 'Low', 'Close', 'Volume'])
df.rename(columns={'Open':'open', 'High':'high', 'Low':'low', 'Close':'close',
                    'Volume':'volume' }, inplace = True) #更改欄位名稱

# Calculate RSI
rsi_period = 14
df['RSI'] = talib.RSI(df['close'], timeperiod=rsi_period)

print("----------")
print(df['RSI'])

plt.figure(figsize=(12, 6))
plt.plot(df.index, df['RSI'], label='RSI', color='blue')
plt.axhline(30, color='red', linestyle='--', label='Overbought (30)')
plt.axhline(70, color='green', linestyle='--', label='Oversold (70)')
plt.title('Relative Strength Index (RSI)')
plt.xlabel('Date')
plt.ylabel('RSI Value')
plt.legend()
plt.show()
print("----------")


# Calculate EMA
ema_period = 14
df['EMA'] = talib.EMA(df['close'], timeperiod=ema_period)

# Plot EMA
plt.figure(figsize=(12, 6))
plt.plot(df.index, df['EMA'], label='EMA', color='blue')
plt.title('Exponential Moving Average (EMA)')
plt.xlabel('Date')
plt.ylabel('EMA Value')
plt.legend()
plt.show()

def drawEMA(xValues, yValues, target_stock):
    plt.figure(figsize=(12, 5))
    plt.title(target_stock, size=15)
    plt.plot(xValues, yValues, '-', color='r', label="EMA")
    plt.legend(loc="best", fontsize=12)
    plt.show()

# Plot EMA
drawEMA(df.index, df['EMA'], target_stock)

#畫出股價序列圖
print(df)

#將df與target_stockt傳入函數，畫出股價序列圖
drawStockSeries(df, target_stock)

closePrices = df.iloc[:, 3].astype('float').values #close price

close_sma_5 = np.round(talib.SMA(closePrices, timeperiod=5), 2)
close_sma_10 = np.round(talib.SMA(closePrices, timeperiod=10), 2)
close_sma_20 = np.round(talib.SMA(closePrices, timeperiod=20), 2)
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
#drawMA5_10_20Series(xpt, ypt1, ypt2, ypt3, target_stock)

#set up the variables for deal
flage = 0
buyPrice = 0
sellPrice = 0
winTime = 0
lossTime = 0
culReturn = 0
transList = []
everyTranReturn = []
tradingDetails = []
tax = 0

for x in range (15, len(df)): #for every single trade day

    if flage==0:    #status: 0 stock
        #close_sma_5[x] > close_sma_10[x] and close_sma_10[x] > close_sma_20[x] and
        #close_sma_10[x] > close_sma_20[x] and
        #df['RSI'][x]> rsi_buy_threshold
        if  df['EMA'][x] > df['EMA'][x - 1]:
            buyPrice = df['close'][x]           #store buy price
            print("買進日期=", str(df.iloc[x:x+1].index[0])[:11],
                  "買進價格=",df.iat[x,3])
            tradingDetails.append(("買進日期=", str(df.index[x])[:10],
                                   "買進價格=", format(buyPrice, ".2f")))
            tax = tax + buyPrice * 0.001425 # store buy transaction fee
            flage =1
    if flage == 1:
        sellPrice = df['close'][x]
        #close_sma_5[x] < close_sma_10[x] and close_sma_10[x] < close_sma_20[x] and
        #close_sma_10[x] < close_sma_20[x] and
        #df['RSI'][x] < rsi_sell_threshold:
        if  df['EMA'][x] < df['EMA'][x - 1]:
            tax = tax + sellPrice*0.001425 + sellPrice * 0.003
            if (sellPrice - buyPrice)>0:
                tradingDetails.append(("賣出日期=", str(df.index[x])[:10],
                                      "賣出價格=", format(sellPrice,".2f"),
                                      "賺=", format((sellPrice-buyPrice-tax), ".2f"),
                                      "Return: ", format((sellPrice-buyPrice-tax)/buyPrice, ".2%")))
                winTime+=1
            else:
                tradingDetails.append(("賣出日期=", str(df.index[x])[:10],
                                       "賣出價格=", format(sellPrice,".2f"),
                                       "賠=", format((sellPrice-buyPrice-tax), ".2f"),
                                      "Return: ", format((sellPrice-buyPrice-tax)/buyPrice, ".2%")))
                lossTime+=1
            flage = 0
            everyTranReturn.append((sellPrice-buyPrice)-tax)
            culReturn = culReturn + (sellPrice - buyPrice) - tax
            transList.append(culReturn)
            tax = 0
            
        if stopLoss>0 and flage ==1:
            if (sellPrice - buyPrice -tax)/buyPrice<-stopLoss:
                tradingDetails.append(("賣出日期=", str(df.index[x])[:10],
                                      "賣出價格=", format(sellPrice,".2f"),
                                      "賺=", format((sellPrice-buyPrice-tax), ".2f"),
                                      "Return: ", format((sellPrice-buyPrice-tax)/buyPrice, ".2%")))
                lossTime+=1
                flage = 0
                everyTranReturn.append((sellPrice-buyPrice)-tax)
                culReturn = culReturn + (sellPrice - buyPrice) - tax
                transList.append(culReturn)
                tax = 0
for i in tradingDetails:
    print(i)

def printStatisticTradingInfor(culReturn, winTime, lossTime, lastClosePrice, firstClosePrice, everyTranReturn):
    print("========================================================================== ")
    print("Final return = ",format(culReturn, ".2f"), "WinTime = ", winTime, "LossTime = ", lossTime )
    print("Buy and Hold = ", (format(lastClosePrice - firstClosePrice, ".2f")))
    print("Maximum Profit = ", format(max(everyTranReturn),".2f"), \
            "Maximum Draw Down = ", format(min(everyTranReturn), ".2f"))
    print("Mean Profit = ", format(np.mean(everyTranReturn), ".2f"), \
            "STD Profit = ", format(np.std(everyTranReturn), ".2f"))
    print("Mean:", format(statistics.mean(everyTranReturn), ".2f"))
    print("variance:", format(statistics.variance(everyTranReturn), ".2f"))
    print("stdev:", format(statistics.stdev(everyTranReturn), ".2f"))
    print("========================================================================== ")
        
printStatisticTradingInfor(culReturn, winTime, lossTime, closePrices[-1], closePrices[0], everyTranReturn)
      


