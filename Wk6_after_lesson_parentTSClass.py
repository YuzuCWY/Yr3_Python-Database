import numpy as np
import pandas as pd
import talib #技術指標套件
from talib import abstract
import yfinance as yf #股價下載套件
from datetime import datetime
from pandas_datareader import data #資料讀取套件
import pandas as pd
import matplotlib.pyplot as plt #畫圖套件
import statistics #統計函數套件
import Wk5_afterlesson_tryconclude

#建立父類別 – parentTSClass.py (Cont.)

class parentTSClass:
    def __init__(self, target_stock, start_date, end_date, stopLoss):
        self.TSmanagerDic = {"1":"1","2":"2"}
        self.target_stock = "2498.TW"
        self.target_stock=target_stock
        self.start_date=start_date
        self.end_date = end_date
        self.stopLoss = stopLoss

    #畫出股價序列圖
    def drawStockSeries(self, df, xLabel):
        df[['close']].plot(figsize=(7,3))
        plt.title(xLabel, size=15)
        plt.legend(loc = "best", fontsize=12)
        plt.show()

    def drawMA5_10_20Series(self, xValues, yValues1, yValues2, yValues3, target_stock):
        plt.figure(figsize=(7,3))
        plt.title(target_stock, size=15)
        plt.plot(xValues,yValues1,'-', color = 'r', label="MA-5") #畫線
        plt.plot(xValues,yValues2,'+', color = 'g', label="MA-10") #畫線
        plt.plot(xValues,yValues3,'x', color = 'b', label="MA-20") #畫線
        plt.legend(loc = "best", fontsize=12)
        plt.show() #顯示繪製的圖形

    def printEveryTradingInfor(self, tradingDetails): #印出儲存在tradingDetails列中的資訊
        for i in tradingDetails:
            for j in i:
                print(j, end=" ")
            print()
    def printStatisticTradingInfor(self, culReturn, winTime, lossTime, lastClosePrice, firstClosePrice, everyTranReturn):
        print("========================================================================== ")
        print("Final return = ",format(culReturn, ".2f"), "WinTime = ", winTime, "LossTime = ", lossTime )
        print("Buy and Hold = ", (format(lastClosePrice - firstClosePrice, ".2f")))
        print("Maximum Profit = ", format(max(everyTranReturn),".2f"),
              "Maximum Draw Down = ", format(min(everyTranReturn), ".2f"))
        print("Mean Profit = ", format(np.mean(everyTranReturn), ".2f"), 
              "STD Profit = ", format(np.std(everyTranReturn), ".2f"))
        print("Mean:", format(statistics.mean(everyTranReturn), ".2f"))
        print("variance:", format(statistics.variance(everyTranReturn), ".2f"))
        print("stdev:", format(statistics.stdev(everyTranReturn), ".2f"))
        print("========================================================================== ")

    def drawCumulativeReturnSeries(self, yValues1):
        plt.title("Cumulative Return", size=15)
        plt.xlabel('Transaction#')
        plt.ylabel('NT$')
        plt.plot(yValues1) #畫線
        plt.show() #顯示繪製的圖形
        
    def tradingStrategy(): # 這函數很重要一定不能少，後面建立多型用
        print()
