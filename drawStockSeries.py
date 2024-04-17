def drawStockSeries(df, xLabel):
    df[['close']].plot(figsize=(7,3))
    plt.title(xLabel, size=15)
    plt.legend(loc = "best", fontsize=12)
    plt.show()
