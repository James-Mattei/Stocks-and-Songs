import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime
import plotly.graph_objects as go
import chart_studio
import chart_studio.plotly as py

def main():

    with open("FullData.csv", "r") as file:
        df = pd.read_csv(file)

    vals = {"foodservice":0, "automobile":1, "clothing":2, "accessories":3, "hospitality":4, 
    "cosmetics":5, "department":6, "sports":7, "footwear":8, "ecommerce":9, "outdoor":10, "electronics":11}

    #filter down datat set to weeks where the brand is mentioned
    mentions = df.loc[df["num_mentions"]>0]
    mentions = mentions.reset_index()
    industry(mentions, vals)

    #Format the parallel coordniate plot
    fig = px.parallel_coordinates(mentions, color='indNum',
    dimensions=['unique_songs', 'num_mentions', 'Increase_This_Week', 'consecutive_weeks'],
    color_continuous_scale=px.colors.diverging.Portland,
    color_continuous_midpoint=2)

    #Upload graph to plotly to embed it in website
    username = 'jam580'
    api_key = 'N0vDnbORLSc0eGxH7Gzg'

    chart_studio.tools.set_credentials_file(username=username, api_key=api_key)
    py.plot(fig, filename = 'ParallelCoord', auto_open=True)

    fig.show()

#Create new column of numeric values of each industry for color mapping for plot
def industry(df, industryDict):
    indust = pd.DataFrame(columns=["indNum"])
    for i in range(0 , len(df), 1):
        indust = indust.append({"indNum": industryDict[df["industry"][i]]}, ignore_index=True)
    df["indNum"] = indust["indNum"].values

if __name__ == "__main__":
    main()