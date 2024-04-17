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
