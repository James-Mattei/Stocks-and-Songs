import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import pearsonr

def main():
    with open("FullData.csv", "r") as file:
        df = pd.read_csv(file)
    
    correlations(df)

    with open("attributes.csv", "r") as file:
        summar = pd.read_csv(file)
    
    with open("Tickers.csv") as file:
        stocks = pd.read_csv (file)

    #Create Mean 
    avgStockPrice(stocks,summar,"mean_transactions")
    avgStockPrice(stocks,summar,"mean_low")
    avgStockPrice(stocks,summar,"mean_high")
    avgStockPrice(stocks,summar,"mean_close")

    print(stocks)
    Hists(stocks, df)

def correlations(df):
    #Correlates percent change in price with volume transactions

    cols = [0,1,2,3,4,5,6,7,8,10,12,13,14,15]
    corrdf = df.drop(df.columns[cols], axis=1)
    print(corrdf.corr(method='pearson'))
    
    corrdf.plot.scatter(x='Delta_Price', y='num_mentions')
    plt.title("Delta_Price vs num_mentions")
    plt.show()
    plt.clf()

    corrdf.plot.scatter(x='Delta_Price', y='consecutive_weeks')
    plt.title("Delta_Price vs consecutive_weeks")
    plt.show()
    plt.clf()

    corrdf.plot.scatter(x='num_mentions', y='consecutive_weeks')
    plt.title("num_mentions vs consecutive_weeks")
    plt.show()
    plt.clf()



def Hists(stocks, df): 

    #Hist of Mean monthly Transactions, there are outliers 
    stocks.hist(column='Monthly_mean_transactions', bins=40)
    plt.xlabel('Mean Monthly Transactions (in 100 millions)')
    plt.ylabel('Number of Stocks')
    plt.title('Histogram of Mean Monthly Transaction per Stock')
    plt.show()
    plt.clf()

    #Hist of Mean monthly closing price
    stocks.hist(column='Monthly_mean_close', bins=40)
    plt.xlabel('Mean Monthly Closing Price ($)')
    plt.ylabel('Number of Stocks')
    plt.title('Histogram of Mean Monthly Closing Price per Stock')
    plt.show()
    plt.clf()

    #Hist of number of mentions per week
    df.hist(column='num_mentions', bins=40)
    plt.xlabel('Number of Mentions in Top 100 Songs')
    plt.ylabel('Number of Weeks')
    plt.title('Histogram of Number of Brand Mentions per Week')
    plt.show()
    plt.clf()

    #Hist of log transformed number of transactions
    df.hist(column='log_volume', bins=40)
    plt.xlabel('Log Number of Transactions')
    plt.ylabel('Number of Weeks')
    plt.title('Histogram of Log(Transactions) per Week')
    plt.show()

#Used to get Average monthly attriburte for Hists
def avgStockPrice(companies, stock, attribute):
    avgprice = pd.DataFrame(columns=["Monthly_"+attribute])
    #For each Stock
    for row in companies['ticker']:
        count = 0
        sum = 0
        for i in range(0, len(stock),1): #Go through monthly attributes data
            if row == stock['ticker'][i]: #Match by ticker
                sum+=stock[attribute][i]
                count+=1
        avg = sum/count
        avgprice= avgprice.append({"Monthly_"+attribute: avg}, ignore_index=True)
    companies["Monthly_"+attribute] = avgprice["Monthly_"+attribute].values #append to old df

if __name__ == "__main__":
    main()