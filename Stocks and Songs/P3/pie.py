import pandas as pd
import numpy as np
import plotly.graph_objects as go

#This file creates the Pie chart that shows the industry makeup of our stock data.

def main():
    #read in primary dataframe
    with open("FullData.csv", "r") as file:
        df = pd.read_csv(file)

    #extract industry names and counts of stocks belonging to that industry
    indLabel=df["industry"].value_counts().index
    indVal=df["industry"].value_counts().tolist()

    #pick out colors
    col=["#07F2C7","#17A697","#85A2A6","#93CFC2","#C1DED9",  "#84A296","#B7CDC1","#EAE6DA","#F5F5EC","#F0B88C","#D9CEB0","#F2DDB6"]
    col2=["#07F2C7","#17A697","#85A2A6","#93CFC2","#C1DED9",  "#84A296","#B7CDC1",     "#204E7A","#57385C","#A75265","#EC7263","#FEBE7E"]

    #create chart, choose font, make hole, pull out the 5 small slices
    fig = go.Figure(data=[go.Pie(labels=indLabel, values=indVal,textfont=dict(family="Menlo",size=11),hole=.25,
                pull=[.0, .0, 0.0, 0,    .0, .0, 0.0, 0.1,.1, .1, 0.1, 0.1],text=indLabel,textposition="outside")])
    fig.update_traces(hoverinfo='value',
                    marker=dict(colors=col2,line=dict(color='white', width=1)))

    fig.update_layout(
        title_text="Stock Composition: Number of Stocks per Industry",
        #print number of stocks in center of donut
        annotations=[dict(text="Stocks:"+str(len(df)//52), x=0.5, y=0.5, font_size=20, showarrow=False)])
    fig.show()

if __name__ == "__main__": 
    main()