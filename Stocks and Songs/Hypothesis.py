from scipy.stats import ttest_ind
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import pearsonr

def main():
    with open("FullData.csv", "r") as file:
        df = pd.read_csv(file)
    
    with open("HypStocks.csv", "r") as file:
        stocks = pd.read_csv(file)

    df['mentioned'] = df.apply(lambda row: mention(row), axis=1)
    
    mentioned = df[df['mentioned']==1]
    notmentioned = df[df['mentioned']==0]
    mentclothing = mentioned[mentioned['industry']=='clothing']
    notmentclothing = mentioned[mentioned['industry']=='accessories']

    print("T-test for Change in Price")
    print("mentioned: ", mentioned['Delta_Price'].mean())
    print("not mentioned: ", notmentioned['Delta_Price'].mean())
    print(ttest_ind(mentioned['Delta_Price'], notmentioned['Delta_Price']) )
    print()

    print("T-test for Change in Price for Clothing")
    print("mentioned: ", mentclothing['Delta_Price'].mean())
    print("not mentioned: ", notmentclothing['Delta_Price'].mean())
    print(ttest_ind(mentclothing['Delta_Price'], notmentclothing['Delta_Price']) )
    print()

    print("T-test for Closing Price")
    print("mentioned: ", mentioned['close'].mean())
    print("not mentioned: ", notmentioned['close'].mean())
    print(ttest_ind(mentioned['close'], notmentioned['close']) )
    print()

    print("T-test for log(Transactions)")
    print("mentioned: ", mentioned['log_volume'].mean())
    print("not mentioned: ", notmentioned['log_volume'].mean())
    print(ttest_ind(mentioned['log_volume'], notmentioned['log_volume']) )



def mention(row):
    if row['num_mentions']>0:
        return 1
    else:
        return 0     

if __name__ == "__main__":
    main()