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

    
#Wk5_afterlesson_tryconclude.MA_Strategy("2498.TW", datetime(2021, 1, 1), datetime(2021, 7, 19), 0.1)
#Wk5_afterlesson_tryconclude.ROC_Strategy("2498.TW", datetime(2021, 1, 1), datetime(2021, 7, 19), 0.1) #呼叫ROC策略16. ROC_Strategy(“2498.TW”, datetime(2021, 1, 1), datetime(2021, 7, 19), 0.1) #呼叫ROC策略
#culReturn_EMA = Wk5_afterlesson_tryconclude.EMA_Strategy("2498.TW", datetime(2021, 1, 1), datetime(2021, 7, 19), 0.1)
#culReturn_RSI = Wk5_afterlesson_tryconclude.RSI_Strategy("2498.TW", datetime(2021, 1, 1), datetime(2021, 7, 19), 0.1)
culReturn_KD = Wk5_afterlesson_tryconclude.KD_Strategy("2498.TW", datetime(2021, 1, 1), datetime(2021, 7, 19), 0.1)

#print("3個策略共賺: " , culReturn_EMA+culReturn_RSI+culReturn_KD)


