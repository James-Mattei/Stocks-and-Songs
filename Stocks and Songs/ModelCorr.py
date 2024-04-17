import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

def main():
    with open("FullData.csv", "r") as file:
        df = pd.read_csv(file)

    #Select the variables used in predictive models
    df = df[['num_mentions',  'industry', 'Delta_Price' , 'log_volume',  'consecutive_weeks']]
    print(df)
    #create correlation df
    corr = df.corr()
    sns.set(style="white")

    #Create base plot
    fig, ax = plt.subplots(figsize=(8,8))
    #create color map to be used for the heatmap
    colormap = sns.diverging_palette(220, 10, as_cmap=True)
    sns.heatmap(corr, cmap=colormap, square=True,
    linewidths=.5, cbar_kws={"shrink":.5})
    #Change the y axis labels
    plt.yticks(rotation="horizontal")
    plt.title("Diagonal Correlation Matrix of Terms in NB Model")
    plt.show()

if __name__ == "__main__":
    main()