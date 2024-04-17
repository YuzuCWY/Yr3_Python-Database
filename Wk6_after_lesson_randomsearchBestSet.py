from Wk6_after_lesson_maTSClass import maTSClass
from Wk6_after_lesson_rocTSClass import rocTSClass
from Wk6_after_lesson_emaTSClass import emaTSClass
from Wk6_after_lesson_rsiTSClass import rsiTSClass
from Wk6_after_lesson_kdTSClass import kdTSClass

from datetime import datetime
import random
import copy

def calculateCulReturn(ts):
    return ts.tradingStrategy()

target_stock="2498.TW"
start_date=datetime(2013, 1, 1)
end_date = datetime(2022, 12, 31)
stopLoss = 0.1

def report(target_stock, start_date, end_date, stopLoss):
    numberOfStrategy = 1 # 交易策略數
    maxReturn = -100000 # 紀錄最大報酬
    tspFinal = [] #紀錄最大報酬交易策略組合
    index = 0 #紀錄第幾次找到最高
    candicateTS = {"ts1": emaTSClass(target_stock, start_date, end_date, stopLoss),
                   "ts2": rsiTSClass(target_stock, start_date, end_date, stopLoss),
                   "ts3": kdTSClass(target_stock, start_date, end_date, stopLoss),
                   "ts4": maTSClass(target_stock, start_date, end_date, stopLoss),
                   "ts5": rocTSClass(target_stock, start_date, end_date, stopLoss)}

    for i in range(0, 5):
        count = 0
        returnSum = 0
        tsp = []
        print("#" + str(i))
        while count != numberOfStrategy:
            numTS = i+1
            #numTS = random.randint(1, len(candicateTS))
            if candicateTS.get("ts"+str(numTS)) not in tsp:
                tsp.append(candicateTS.get("ts"+str(numTS)))
                returnSum = returnSum + calculateCulReturn(candicateTS.get("ts"+str(numTS)))
                count += 1
        print("returnSum = ", returnSum)
        if returnSum > maxReturn:
            maxReturn = returnSum
            tspFinal = copy.deepcopy(tsp)
            index = i
        print()

    #print("上漲趨勢回測區間最佳報酬: ")
    print("#", index, "has maxReturn =", format(maxReturn,".2f"))
    print("Selected Final TSP = ", tspFinal)

print("上漲趨勢回測區間最佳報酬: ")
report("2330.TW", datetime(2013, 1, 1), datetime(2022, 12, 31), 0.1)
print("-------------------------------------------------")

print("盤整趨勢回測區間最佳報酬: ")
report("2412.TW", datetime(2013, 1, 1), datetime(2022, 12, 31), 0.1)
print("-------------------------------------------------")

print("下跌趨勢回測區間最佳報酬: ")
report("2498.TW", datetime(2013, 1, 1), datetime(2022, 12, 31), 0.1)
print("-------------------------------------------------")
