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
##    global flage
##    global buyPrice
##    global sellPrice
##    global winTime
##    global loseTime
##    global culReturn
##    global transList
##    global everyTranReturn
##    global tradingDetails
##    global tax
##    global closePrices

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
                tradingDetails.append(("買進日期 = ", str(df.iloc[x:x+1].index[0])[:11] , 
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
    return culReturn
    
def ROC_Strategy(target_stock, start_date, end_date, stopLoss):

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
                    tax=0
    #印出逐筆交易資訊，程式碼在後面第6頁
    printEveryTradingInfor(tradingDetails)
    #印出交易統計資訊，程式碼在後面第7頁
    printStatisticTradingInfor(culReturn, winTime, lossTime, closePrices[-1], closePrices[0], everyTranReturn)
    #印出累計報酬圖，程式碼在後面第8頁
    drawCumulativeReturnSeries(transList)
    return culReturn

def EMA_Strategy(target_stock, start_date, end_date, stopLoss):
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
    
    #利用talib計算ROC值
    closePrices = df.iloc[:, 3].astype('float').values #收盤價
    
    # Set EMA thresholds for buy and sell signals
    ema_buy_threshold = 5
    ema_sell_threshold = 10

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
    
    # Plot EMA
    #drawEMA(df.index, df['EMA'], target_stock)
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
    #印出逐筆交易資訊，程式碼在後面第6頁
    printEveryTradingInfor(tradingDetails)
    #印出交易統計資訊，程式碼在後面第7頁
    printStatisticTradingInfor(culReturn, winTime, lossTime, closePrices[-1], closePrices[0], everyTranReturn)
    #印出累計報酬圖，程式碼在後面第8頁
    drawCumulativeReturnSeries(transList)
    return culReturn


def KD_Strategy(target_stock, start_date, end_date, stopLoss):

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

    
    df_kd = abstract.STOCH(df, fastk_period=14, slowk_period=1, slowd_period=3)
    print(df_kd)
    print("TEST")
    print(df_kd['slowk'][-5])
    plt.figure(figsize=(12, 6))
    plt.axhline(80, color='red', linestyle='--', label='Overbought (80)')
    plt.axhline(20, color='green', linestyle='--', label='Oversold (20)')
    plt.plot(df.index, df_kd['slowk'], label='KD Index_K', color='orange')
    plt.plot(df.index, df_kd['slowd'], label='KD Index_D', color='blue')
    plt.title('KD Index')
    plt.xlabel('Date')
    plt.ylabel('KD Value')
    plt.legend()
    plt.show()
    #====================
    
    #買賣策略設定與交易
    for x in range(15, len(closePrices)):#每一個交易天
        if flage == 0: #狀態: 未持有股票
            #多頭排列成立
            #-----------------------------------
            if (df_kd['slowk'][x]>df_kd['slowk'][x-1] and df_kd['slowk'][x]>df_kd['slowd'][x] and df_kd['slowk'][x]>80):
                buyPrice = closePrices[x]#儲存買進價格
                tradingDetails.append(("買進日期 = ", str(df.iloc[x:x+1].index[0])[:11] , 
                                        "買進價格 = ", format(buyPrice, ".2f"))) #紀錄買進資訊
                tax = tax + buyPrice * 0.001425 #儲存買進手續費
                flage = 1#更新狀態
        if flage == 1: #狀態，持有股票
            sellPrice = closePrices[x]
            #--------------------------------------------------
            if (df_kd['slowk'][x]<df_kd['slowk'][x-1] and df_kd['slowk'][x]<df_kd['slowd'][x] and df_kd['slowk'][x]<20):#空頭排列成立
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
    return culReturn

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
    RSI_14 = talib.RSI(df['close'], timeperiod=14)
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
                tradingDetails.append(("買進日期 = ", str(df.iloc[x:x+1].index[0])[:11] , 
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
    return culReturn
    
