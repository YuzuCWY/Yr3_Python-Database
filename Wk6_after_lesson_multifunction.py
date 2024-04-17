from Wk6_after_lesson_maTSClass import maTSClass
from Wk6_after_lesson_rocTSClass import rocTSClass
from datetime import datetime


target_stock="2498.TW"
start_date=datetime(2021, 1, 1)
end_date = datetime(2021, 7, 19)
stopLoss = 0.1

def calcuateCulReturn(ts):
    return ts.tradingStrategy()
ts1 = maTSClass(target_stock, start_date, end_date, stopLoss)
print("CulReturn of TS1:", calcuateCulReturn(ts1))
ts2 = rocTSClass(target_stock, start_date, end_date, stopLoss)
print("CulReturn of TS2:", calcuateCulReturn(ts2))
# 如有設計其它策略類別，只需呼叫同一函數便可計算報酬
