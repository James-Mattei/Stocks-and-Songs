import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn import preprocessing
import pylab as pl
from sklearn import decomposition
from pprint import pprint
from sklearn.metrics import silhouette_samples, silhouette_score

pd.set_option('display.max_columns', 500)
pd.set_option('display.max_rows', 500)
pd.set_option('display.width', 1000)

def main():

    with open("stocks.csv", "r") as file:
        stocks = pd.read_csv(file) 

    with open("attributes.csv", "r") as file:
        attributes = pd.read_csv(file)  
    
    #need all these to centralize your stats from attributes
    avgCol(stocks, attributes, "mean_transactions")
    avgCol(stocks, attributes, "mean_low")
    avgCol(stocks, attributes, "mean_high")
    avgCol(stocks, attributes, "mean_close")

    with open("Cluster.txt", "a+") as outFile:
        KmeanCluster(2, stocks, outFile)
        KmeanCluster(4, stocks, outFile)
        KmeanCluster(6, stocks, outFile)
    #Create updated HypStocks to be used for Hypothesis Testing
    with open("HypStocks.csv", "w") as file:
        stocks.to_csv(file, encoding='utf-8', index=False)

def logTransform(row, header):
    if(row[header]!=0):
      return np.log(row[header])
    return 0

def normalize(df):
    #Create df to be normalized
    df = pd.concat([df["mean_transactions"], df["mean_low"], df["mean_high"],
    df["mean_close"]], keys= ["mean_transactions", "mean_low",
    "mean_high", "mean_close"], axis=1)

    x = df.values #returns a numpy array
    min_max_scaler = preprocessing.MinMaxScaler() #Min max normalizations
    x_scaled = min_max_scaler.fit_transform(x)
    return pd.DataFrame(x_scaled)

#Calcualte average given column atribute for all stocks
def avgCol(companies, stock, col):
    avgprice = pd.DataFrame(columns=[col])
    for row in companies['ticker']: #For each Stock
        count = 0
        sum = 0
        for i in range(0, len(stock),1): #for each entry in the attributes
            if row == stock['ticker'][i]:
                sum+=stock[col][i]
                count+=1
        avg = sum/count #Create the sum
        avgprice= avgprice.append({col: avg}, ignore_index=True)
    companies[col] = avgprice[col].values #append values to new dataframe

def KmeanCluster(nCluster, df, out):
    normdf = normalize(df) #normalize data
    cluster = KMeans(n_clusters = nCluster)
    labels = cluster.fit_predict(normdf) #Create predictions
    silhouette = silhouette_score(normdf, labels) #Calculate silhouette score
    
    print("Silhouette score for k means clustering with ", nCluster, "centroids is: ",
    silhouette, file=out)
    print("Cluster labels for ", nCluster, " clusters are: \n", labels, file = out)

    #Create all the plots
    #Plot 1 - mean_transactions
    plt.clf() #make sure there are no unclosed previous pltos
    plt.subplot(1,4,1) #Creates a sub plot of 1 row, 3 cols, building position 1
    plt.scatter(labels, df["mean_transactions"])
    plt.title("Cluster vs \nMonthly Vol")
    plt.xlabel("Clusters")
    plt.ylabel("Mean transactions")

    #plot 2 - mean_low
    plt.subplot(1,4,2)
    plt.scatter(labels, df["mean_low"])
    plt.title("Cluster vs \nMonthly Low")
    plt.xlabel("Clusters")
    plt.ylabel("Mean Low")

    #plot 3 - mean_high
    plt.subplot(1,4,3)
    plt.scatter(labels, df["mean_high"])
    plt.title("Cluster vs \nMonthly High")
    plt.xlabel("Clusters")
    plt.ylabel("Mean High")

    #plot 4 - mean_close
    plt.subplot(1,4,4)
    plt.scatter(labels, df["mean_close"])
    plt.title("Cluster vs \nMonthly Close")
    plt.xlabel("Clusters")
    plt.ylabel("Mean Close")

    #plt.tight_layout()
    plt.subplots_adjust(wspace = .99) # Addjust spacing so titles will fit
    plt.show()


if __name__ == "__main__":
    main()