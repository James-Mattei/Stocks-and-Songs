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
   

    mentions = df.loc[df["num_mentions"]>0]
    mentions = mentions.reset_index()
    countdf = pd.DataFrame


    countdf = monthlyCount(mentions)
    with open("stackbar.csv", "w") as dataFile:
        countdf.to_csv(dataFile, encoding='utf-8', index=False)

    #wrote output to file to speed up development process
    # with open("stackbar.csv", "r") as file:
    #     countdf = pd.read_csv(file)

    vals = ["foodservice", "automobile", "clothing", "accessories", "hospitality", 
    "cosmetics", "department", "sports", "footwear", "ecommerce", "outdoor", "electronics"]
    fig = go.Figure()
    #Add all the traces for the different industries
    addTraces(fig, countdf, vals)
    
    #change it to stacked bar
    fig.update_layout(barmode='stack')

    #update the layout so that there are buttons for the industries that are mentioned
    fig.update_layout(
        updatemenus=[
            go.layout.Updatemenu(
                type="buttons",
                direction="right",
                active=0,
                x=1,
                y=1.2,
                buttons=list([
                    dict(label="All",
                    method = "update",
                    args=[{"visible": [True,True,True,True,True,True,True,True,True,True,True,True,]},
                    {"title": "Number of Mentions for all Industries"}]),
                    dict(label="Foodservice",
                    method = "update",
                    args=[{"visible": [True,False,False,False,False,False,False,False,False,False,False,False,]},
                    {"title": "Foodservice"}]),
                    dict(label="Automobile",
                    method = "update",
                    args=[{"visible": [False,True,False,False,False,False,False,False,False,False,False,False,]},
                    {"title": "Automobile"}]),
                    dict(label="Clothing",
                    method = "update",
                    args=[{"visible": [False,False,True,False,False,False,False,False,False,False,False,False,]},
                    {"title": "Clothing"}]),
                    dict(label="Accessories",
                    method = "update",
                    args=[{"visible": [False,False,False,True,False,False,False,False,False,False,False,False,]},
                    {"title": "Accessories"}]),
                    dict(label="Cosmetic",
                    method = "update",
                    args=[{"visible": [False,False,False,False,False,True,False,False,False,False,False,False,]},
                    {"title": "Cosmetic"}]),
                    dict(label="Department",
                    method = "update",
                    args=[{"visible": [False,False,False,False,False,False,True,False,False,False,False,False,]},
                    {"title": "Department"}]),
                    dict(label="Sports",
                    method = "update",
                    args=[{"visible": [False,False,False,False,False,False,False,True,False,False,False,False,]},
                    {"title": "Sports"}]),
                    dict(label="Footwear",
                    method = "update",
                    args=[{"visible": [False,False,False,False,False,False,False,False,True,False,False,False,]},
                    {"title": "Footwear"}]),
                    dict(label="Outdoor",
                    method = "update",
                    args=[{"visible": [False,False,False,False,False,False,False,False,False,False,True,False,]},
                    {"title": "Outdoor"}]),
                ])
            )
        ]
    )

    #update the layout to include axis labels and title
    fig.update_layout(
        xaxis_title = "Month",
        yaxis_title = "Number of Mentions",
        title = "Number of Mentions for all Industries"
    )

    fig.show()

    #Code used to upload bar chart for embeding in our website
    # username = 'jam580'
    # api_key = 'N0vDnbORLSc0eGxH7Gzg'

    # chart_studio.tools.set_credentials_file(username=username, api_key=api_key)
    # py.plot(fig, filename = 'Mentions_per_Industry', auto_open=True)


#create a new data frame which has the number of mentions for each industry
#for each month
def monthlyCount(fulldf):
    df = pd.DataFrame()
    #create dataframe columns to be filled
    dates = pd.DataFrame(columns=["month"])
    numcount = pd.DataFrame(columns=["mention"])
    industs = pd.DataFrame(columns=["industry"])
    #create lists for industry and month
    vals = ["foodservice", "automobile", "clothing", "accessories", "hospitality", "cosmetics", "department", "sports", "footwear", "ecommerce", "outdoor", "electronics"]
    month = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    
    for industry in vals:
        hold = fulldf.loc[fulldf["industry"]==industry]
        hold = hold.reset_index()
        for mon in month: #For each month
            count = 0
            for i in range(0, len(hold), 1):
                if hold["date"][i][0:3]==mon: #if the month matches add to the running sum
                    count += hold["num_mentions"][i]
            #Add the values to the dataframe columns
            dates = dates.append({"month": mon}, ignore_index=True)
            industs = industs.append({"industry": industry}, ignore_index=True)
            numcount = numcount.append({"mention": count}, ignore_index=True)
            print("Finished: ", mon, " " , industry)   
    #add the values from the columns to the new data frame and return it
    df["month"] = dates["month"].values
    df["industry"] = industs["industry"].values
    df["mention"] =  numcount["mention"].values       
    return df           


def addTraces(fig, countdf, vals):
    for industry in vals:
        fig.add_trace(
            go.Bar(name=industry, 
            x=countdf["month"], 
            y=countdf.loc[countdf["industry"]==industry]["mention"])
        )

if __name__ == "__main__":
    main()