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

class rocTSClass(parentTSClass):
    def __init__(self, target_stock, start_date, end_date, stopLoss):
        self.target_stock=target_stock
        self.start_date=start_date
        self.end_date = end_date
        self.stopLoss = stopLoss

    def tradingStrategy(self, target_stock=0, start_date=0, end_date=0, stopLoss=0):

        target_stock=self.target_stock
        start_date=self.start_date
        end_date = self.end_date
        stopLoss = self.stopLoss
        
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
        
        #取得股價
        yf.pdr_override()
        df = data.get_data_yahoo([target_stock], start_date, end_date)
        df = df.reindex(columns = ['Open','High', 'Low', 'Close', 'Volume']) #保留所需欄位
        
        #更改欄位名稱
        df.rename(columns={'Open':'open', 'High':'high', 'Low':'low', 'Close':'close', 'Volume':'volume' },
                inplace = True)
        #畫出股價序列圖
        #self.drawStockSeries(df, target_stock)
        
        #利用talib計算ROC值
        closePrices = df.iloc[:, 3].astype('float').values #收盤價
        ROC_10 = talib.ROC(closePrices, timeperiod=12)
        
        #買賣策略設定與交易
        for x in range(10, len(closePrices)):#每一個交易天
            if flage == 0: #狀態: 未持有股票
                if ROC_10[x-1] < 0 and ROC_10[x] > 0:
                    buyPrice = closePrices[x]#儲存買進價格
                    tradingDetails.append(("買進日期 = ", str(df.iloc[x:x+1].index[0])[:11] , 
                                            "買進價格 = ", format(buyPrice, ".2f"))) #紀錄買進資訊
                    tax = tax + buyPrice * 0.001425 #儲存買進手續費
                    flage = 1#更新狀態
            if flage == 1: #狀態，持有股票
                sellPrice = closePrices[x]
                if ROC_10[x-1] > 0 and ROC_10[x] < 0:
                    tax = tax + sellPrice * 0.001425 + sellPrice*0.003 #計算交易成本
                    if ( sellPrice- buyPrice) > 0: #報酬為正
                        tradingDetails.append(("賣出日期 = ", str(df.iloc[x:x+1].index[0])[:11] ,
                                               "賣出價格 = ", format(sellPrice, ".2f"),
                                               "賺", format(( sellPrice- buyPrice-tax),".2f"),
                                               format(( sellPrice- buyPrice-tax) / buyPrice, ".2%"))) #紀錄賣出資訊
                        winTime+=1 #獲勝次數+1
                    else: #報酬為負
                        tradingDetails.append(("賣出日期 = ", str(df.iloc[x:x+1].index[0])[:11] ,
                                               "賣出價格 = ", format(sellPrice, ".2f"),
                                               "賠", format(( sellPrice- buyPrice-tax),".2f"),
                                               format(( sellPrice- buyPrice-tax) / buyPrice, ".2%")))
                        lossTime+=1 #失敗次數+1
                    flage = 0 #更新成未持有股票
                    everyTranReturn.append(( sellPrice- buyPrice)- tax) #儲存每筆交易獲利
                    culReturn = culReturn + ( sellPrice- buyPrice)- tax #計算累計獲利
                    transList.append(culReturn) #儲存每次的累計獲利
                    tax = 0 #完成交易, 成本變數歸零
                if stopLoss > 0 and flage == 1:
                    if (sellPrice- buyPrice-tax) / buyPrice <-stopLoss: #停損條件成立
                        tradingDetails.append(("賣出日期 = ", str(df.iloc[x:x+1].index[0])[:11] ,
                                               "賣出價格 = ", format(sellPrice, ".2f"),
                                               "賺",format(( sellPrice- buyPrice-tax),".2f"),
                                               format(( sellPrice- buyPrice-tax) / buyPrice, ".2%"))) #紀錄賣出資訊
                        lossTime+=1
                        flage = 0
                        everyTranReturn.append(( sellPrice- buyPrice)- tax)
                        culReturn = culReturn + ( sellPrice- buyPrice)- tax
                        transList.append(culReturn)
                        tax = 0
        #印出逐筆交易資訊，程式碼在後面第6頁
        #self.printEveryTradingInfor(tradingDetails)
        #印出交易統計資訊，程式碼在後面第7頁
        #self.printStatisticTradingInfor(culReturn, winTime, lossTime, closePrices[-1], closePrices[0], everyTranReturn)
        #印出累計報酬圖，程式碼在後面第8頁
        #self.drawCumulativeReturnSeries(transList)
        return culReturn

