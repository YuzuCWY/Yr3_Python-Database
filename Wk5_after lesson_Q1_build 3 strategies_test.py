import numpy as np
import pandas as pd
import talib #技術指標套件
import yfinance as yf #股價下載套件
from datetime import datetime
from pandas_datareader import data #資料讀取套件
import pandas as pd
import matplotlib.pyplot as plt #畫圖套件
import statistics #統計函數套件
import drawCumulativeReturnSeries, drawMA5_10_20Series

def drawCumulativeReturnSeries(yValues1):
    plt.title("Cumulative Return", size=15)
    plt.xlabel('Transaction#')
    plt.ylabel('NT$')
    plt.plot(yValues1) #畫線
    plt.show() #顯示繪製的圖形

def drawMA5_10_20Series(xValues, yValues1, yValues2, yValues3, target_stock):
    plt.figure(figsize=(7,3))
    plt.title(target_stock, size=15)
    plt.plot(xValues,yValues1,'-', color = 'r', label="MA-5") #畫線
    plt.plot(xValues,yValues2,'+', color = 'g', label="MA-10") #畫線
    plt.plot(xValues,yValues3,'x', color = 'b', label="MA-20") #畫線
    plt.legend(loc = "best", fontsize=12)
    plt.show() #顯示繪製的圖形

def drawStockSeries(df, xLabel):
    df[['close']].plot(figsize=(7,3))
    plt.title(xLabel, size=15)
    plt.legend(loc = "best", fontsize=12)
    plt.show()

def printEveryTradingInfor(tradingDetails): #印出儲存在tradingDetails列中的資訊
    for i in tradingDetails:
        for j in i:
            print(j, end=" ")
        print()
        
def drawEMA(xValues, yValues, target_stock):
    plt.figure(figsize=(12, 5))
    plt.title(target_stock, size=15)
    plt.plot(xValues, yValues, '-', color='r', label="EMA")
    plt.legend(loc="best", fontsize=12)
    plt.show()
    
def printStatisticTradingInfor(culReturn, winTime, lossTime, lastClosePrice, firstClosePrice, everyTranReturn):
    print("========================================================================== ")
    print("Final return = ",format(culReturn, ".2f"), "WinTime = ", winTime, "LossTime = ", lossTime )
    print("Buy and Hold = ", (format(lastClosePrice - firstClosePrice, ".2f")))
    print("Maximum Profit = ", format(max(everyTranReturn),".2f"), \
            "Maximum Draw Down = ", format(min(everyTranReturn), ".2f"))
    print("Mean Profit = ", format(np.mean(everyTranReturn), ".2f"), 
            "STD Profit = ", format(np.std(everyTranReturn), ".2f"))
    print("Mean:", format(statistics.mean(everyTranReturn), ".2f"))
    print("variance:", format(statistics.variance(everyTranReturn), ".2f"))
    print("stdev:", format(statistics.stdev(everyTranReturn), ".2f"))
    print("========================================================================== ")

def MA_Strategy(target_stock, start_date, end_date, stopLoss):

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
    drawStockSeries(df, target_stock)
    #利用talib計算移動平均線，並畫出5、10、20MA圖
    closePrices = df.iloc[:, 3].astype('float').values #收盤價
    close_sma_5 = np.round(talib.SMA(closePrices, timeperiod=5), 2)
    close_sma_10 = np.round(talib.SMA(closePrices, timeperiod=10), 2)
    close_sma_20 = np.round(talib.SMA(closePrices, timeperiod=20), 2)
    #利用matplotlib畫出移動平均線
    drawMA5_10_20Series(df.index, close_sma_5, close_sma_10, close_sma_20,
                        target_stock)


    #====================
    #買賣策略設定與交易
    for x in range(19, len(closePrices)):#每一個交易天
        if flage == 0: #狀態: 未持有股票
            #多頭排列成立
            if close_sma_5[x] > close_sma_10[x] and close_sma_10[x] > close_sma_20[x]:
                buyPrice = closePrices[x]#儲存買進價格
                tradingDetails.append(("買進日期 = ", str(df.iloc[x:x+1].index[0])[:11] , \
                                        "買進價格 = ", format(buyPrice, ".2f"))) #紀錄買進資訊
                tax = tax + buyPrice * 0.001425 #儲存買進手續費
                flage = 1#更新狀態
        if flage == 1: #狀態，持有股票
            sellPrice = closePrices[x]
            if close_sma_5[x] < close_sma_10[x] and close_sma_10[x] < close_sma_20[x]:#空頭排列成立
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
                    tax = 0 #完成交易, 成本變數歸零
                    
    #印出逐筆交易資訊，程式碼在後面第6頁
    printEveryTradingInfor(tradingDetails)
    #印出交易統計資訊，程式碼在後面第7頁
    printStatisticTradingInfor(culReturn, winTime, lossTime, closePrices[-1], closePrices[0], everyTranReturn)

    #印出累計報酬圖，程式碼在後面第8頁
    drawCumulativeReturnSeries(transList)

    
def RSI_Strategy(target_stock, start_date, end_date, stopLoss):

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
    drawStockSeries(df, target_stock)
    
    #利用talib計算移動平均線，並畫出5、10、20MA圖
    closePrices = df.iloc[:, 3].astype('float').values #收盤價
    
    # Calculate RSI
    rsi_period = 14
    RSI_14 = talib.RSI(df['close'], timeperiod=rsi_period)
    RSI_6 = talib.RSI(df['close'], timeperiod=6)
    print("----------")
    print(RSI_14)
    print(RSI_6)

    #利用matplotlib畫出移動線
    plt.figure(figsize=(12, 6))
    plt.plot(df.index, RSI_6, label='RSI', color='blue')
    plt.axhline(30, color='red', linestyle='--', label='Overbought (30)')
    plt.axhline(70, color='green', linestyle='--', label='Oversold (70)')
    plt.title('Relative Strength Index (RSI6)')
    plt.xlabel('Date')
    plt.ylabel('RSI Value')
    plt.legend()
    plt.show()
    
    #利用matplotlib畫出移動線
    plt.figure(figsize=(12, 6))
    plt.plot(df.index, RSI_14, label='RSI', color='blue')
    plt.axhline(30, color='red', linestyle='--', label='Overbought (30)')
    plt.axhline(70, color='green', linestyle='--', label='Oversold (70)')
    plt.title('Relative Strength Index (RSI14)')
    plt.xlabel('Date')
    plt.ylabel('RSI Value')
    plt.legend()
    plt.show()

    

    #====================
    #買賣策略設定與交易
    for x in range(15, len(closePrices)):#每一個交易天
        if flage == 0: #狀態: 未持有股票
            #多頭排列成立
            #-----------------------------------
            if RSI_14[x]-RSI_14[x - 1] > 0 and RSI_14[x]>=30 and RSI_6[x]>RSI_14[x]:
                buyPrice = closePrices[x]#儲存買進價格
                tradingDetails.append(("買進日期 = ", str(df.iloc[x:x+1].index[0])[:11] , \
                                        "買進價格 = ", format(buyPrice, ".2f"))) #紀錄買進資訊
                tax = tax + buyPrice * 0.001425 #儲存買進手續費
                flage = 1#更新狀態
        if flage == 1: #狀態，持有股票
            sellPrice = closePrices[x]
            #--------------------------------------------------
            if RSI_14[x]-RSI_14[x - 1] <= 0 and RSI_14[x-1]>=70 and RSI_6[x]<=RSI_14[x]:#空頭排列成立
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
                everyTranReturn.append((sellPrice- buyPrice)- tax) #儲存每筆交易獲利
                culReturn = culReturn + (sellPrice- buyPrice)- tax #計算累計獲利
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
                    tax = 0 #完成交易, 成本變數歸零
                    
    #印出逐筆交易資訊，程式碼在後面第6頁
    printEveryTradingInfor(tradingDetails)
    #印出交易統計資訊，程式碼在後面第7頁
    printStatisticTradingInfor(culReturn, winTime, lossTime, closePrices[-1], closePrices[0], everyTranReturn)

    #印出累計報酬圖，程式碼在後面第8頁
    drawCumulativeReturnSeries(transList) 




#MA_Strategy("2498.TW", datetime(2021, 1, 1), datetime(2021, 7, 19), 0.1)
#ROC_Strategy("2498.TW", datetime(2021, 1, 1), datetime(2021, 7, 19), 0.1) #呼叫ROC策略16. ROC_Strategy(“2498.TW”, datetime(2021, 1, 1), datetime(2021, 7, 19), 0.1) #呼叫ROC策略
#EMA_Strategy("2498.TW", datetime(2021, 1, 1), datetime(2021, 7, 19), 0.1)
RSI_Strategy("2498.TW", datetime(2021, 1, 1), datetime(2021, 7, 19), 0.1)

