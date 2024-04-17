def drawMA5_10_20Series(xValues, yValues1, yValues2, yValues3, target_stock):
    plt.figure(figsize=(7,3))
    plt.title(target_stock, size=15)
    plt.plot(xValues,yValues1,'-', color = 'r', label="MA-5") #畫線
    plt.plot(xValues,yValues2,'+', color = 'g', label="MA-10") #畫線
    plt.plot(xValues,yValues3,'x', color = 'b', label="MA-20") #畫線
    plt.legend(loc = "best", fontsize=12)
    plt.show() #顯示繪製的圖形
