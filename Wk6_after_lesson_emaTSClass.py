import numpy as np
import pandas as pd
import talib
import yfinance as yf
from datetime import datetime
from pandas_datareader import data
import pandas as pd
import matplotlib.pyplot as plt
import statistics
from Wk6_after_lesson_parentTSClass import parentTSClass

class emaTSClass(parentTSClass):
    def __init__(self, target_stock, start_date, end_date, stopLoss):
        self.target_stock=target_stock
        self.start_date=start_date
        self.end_date = end_date
        self.stopLoss = stopLoss

    #EMA_Strategy
    def tradingStrategy(self, target_stock=0, start_date=0, end_date=0, stopLoss=0):
        target_stock=self.target_stock
        start_date=self.start_date
        end_date = self.end_date
        stopLoss = self.stopLoss
        #取得股價
        yf.pdr_override()
        df = data.get_data_yahoo([target_stock], start_date, end_date)
        df = df.reindex(columns = ['Open','High', 'Low', 'Close', 'Volume'])
        df.rename(columns={'Open':'open', 'High':'high', 'Low':'low', 'Close':'close',
                           'Volume':'volume' }, inplace = True)
        #畫出股價序列圖
        #self.drawStockSeries(df, target_stock)

        #利用talib計算移動平均線，並畫出5、10、20MA圖
        closePrices = df.iloc[:, 3].astype('float').values #收盤價

        #設定交易所需要用的變數
        flage = 0 # 判斷目前是否有持股
        buyPrice = 0
        sellPrice = 0
        winTime = 0 #交易賺錢次數
        lossTime = 0 #交易虧損次數
        culReturn = 0 #第k次交易之累計報酬
        transList = [] #每次交易之累計報酬
        everyTranReturn = [] #每筆交易報酬
        tradingDetails = [] #紀錄每筆交易詳細資訊, 日期, 股價, 獲利等
        tax = 0 #交易成本
        #====================
        
        # Set EMA thresholds for buy and sell signals
        ema_buy_threshold = 5
        ema_sell_threshold = 10

        # Calculate EMA
        ema_period = 14
        df['EMA'] = talib.EMA(df['close'], timeperiod=ema_period)
        
        # Plot EMA
        #drawEMA(df.index, df['EMA'], target_stock)
        
        for x in range (15, len(df)): #for every single trade day
            if flage==0:    #status: 0 stock
                #close_sma_5[x] > close_sma_10[x] and close_sma_10[x] > close_sma_20[x] and
                #close_sma_10[x] > close_sma_20[x] and
                #df['RSI'][x]> rsi_buy_threshold
                if  df['EMA'][x] > df['EMA'][x - 1]:
                    buyPrice = df['close'][x]           #store buy price
                    #print("買進日期=", str(df.iloc[x:x+1].index[0])[:11],
                          #"買進價格=",df.iat[x,3])
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
        #印出逐筆交易資訊，程式碼在後面第6頁
        #printEveryTradingInfor(tradingDetails)
        #印出交易統計資訊，程式碼在後面第7頁
        #printStatisticTradingInfor(culReturn, winTime, lossTime, closePrices[-1], closePrices[0], everyTranReturn)
        #印出累計報酬圖，程式碼在後面第8頁
        #drawCumulativeReturnSeries(transList)
        return culReturn
