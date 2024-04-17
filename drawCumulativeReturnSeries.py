def drawCumulativeReturnSeries(yValues1):
    plt.title("Cumulative Return", size=15)
    plt.xlabel('Transaction#')
    plt.ylabel('NT$')
    plt.plot(yValues1) #畫線
    plt.show() #顯示繪製的圖形
