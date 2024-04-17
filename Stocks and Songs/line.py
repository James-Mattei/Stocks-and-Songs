import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import ast
import copy
import chart_studio
import chart_studio.plotly as py

#creates line plot of avg sentiment score for all songs, for songs that mention brands, and songs that don't.

def plot(WeekLabel,AvgSongLabel,AvgMentLabel,AvgNotLabel):
    fig=go.Figure()

    fig.add_trace(go.Scatter(x=WeekLabel,y=AvgSongLabel,mode='lines',name="Average Total Sentiment Score"))
    fig.add_trace(go.Scatter(x=WeekLabel,y=AvgMentLabel,mode='lines',name="Average Mentioned Sentiment Score"))
    fig.add_trace(go.Scatter(x=WeekLabel,y=AvgNotLabel,mode='lines',name="Average Not Mentioned Sentiment Score"))

    fig.update_layout(
        title="Sentiment Scores for Songs that Do and Don't Mention Brands",
        xaxis_title="Week Number",
        yaxis_title="Average Sentiment Score",
    )
    #Code used to upload bar chart for embeding in our website
    username = 'jam580'
    api_key = 'N0vDnbORLSc0eGxH7Gzg'

    chart_studio.tools.set_credentials_file(username=username, api_key=api_key)
    py.plot(fig, filename = 'lineGraph', auto_open=True)
    fig.show()
def getAvg(weekToSongList,dictionary):
    AvgSongLabel=[]
    for k in weekToSongList.keys(): #for all weeks
        sL=weekToSongList[k] #extract the song list
        Sum=0
        Valid=0
        for song in sL: #iterate over all provided songs
            try:
                Sum+=dictionary[str(song[0])] #try to do a sentiment score lookup
                Valid+=1
            except:
                try:
                    Sum+=dictionary[str(song[0]).upper()] #reformat and try again
                    Valid+=1
                except:
                    try:
                        Sum+=dictionary[str(song[0]).lower()]
                        Valid+=1
                    except:
                        pass #else do nothing
        try:
            AvgSongLabel.append((k,Sum/Valid))
        except:
            AvgSongLabel.append((k,np.nan)) #if no valid, null
    return AvgSongLabel
def getMentionedAndNotMentioned():
    with open("SongsTickerMentions.csv", "r") as file:
        df2 = pd.read_csv(file)

    df2.drop(columns="Artist",inplace=True)

    colList=[x for x in df2][1:]

    Mentioned=[]
    NotMentioned=[]
    for index, row in df2.iterrows():
        for col in colList:
            if row[col] > 0: #if more than one mention
                Mentioned.append(df2.iloc[index]["Song"])
                break

    for s in Mentioned: #drop mentioned songs to be left with not mentioned songs
        df2.drop((df2.loc[df2["Song"]==s]).index.tolist()[0],inplace=True)

    NotMentioned=list(df2["Song"])

    return [Mentioned,NotMentioned]
def genNewWeekToSongList(Songs,weekToSongList):
    for k in weekToSongList.keys(): #calculates intersection of all top songs and songs that do or dont brand mention
        temp=[]
        for s in weekToSongList[k]:
            for s2 in Songs:
                if s2 == s[0]: #if song in dict == Ment or !Ment song
                    temp.append(s)
        weekToSongList[k]=temp #overwrite relevant songs
    return weekToSongList

def main():
    #read file containing song names and sentiment scores
    with open("polarity.csv", "r") as file:
        df = pd.read_csv(file)

    #x label: song name
    #y label: sentiment score
    indLabel=list(df["Song"])
    indVal=list(df["polarity"])

    #create an {x:y} mapping of songname to sentiment score
    dictionary = dict(zip(indLabel, indVal))

    #read in songs with respect to the time they were on the top charts
    content=[]
    with open("weeklyData.txt", "r") as file:
        content=file.readlines()
    weekToSongList={}

    #store the lists of songs in a dictionary of {line#inFile :  SongList}
    i=1
    while i < 156:
        if "[" in content[i]:  #if we're on a line with a list, store it.
            weekToSongList[i]=ast.literal_eval(content[i])
        i+=1

    #generate x-axis labels of week number
    WeekLabel=[]
    for i in range(1,53):
        WeekLabel.append("Week "+str(i))

    #get the weekly avg sentiment score for all data
    AvgSongLabel=getAvg(weekToSongList,dictionary)

    #partition the data into songs that do brand mentions and those that dont
    MentionedAndNot=getMentionedAndNotMentioned()
    Mentioned=MentionedAndNot[0]
    NotMentioned=MentionedAndNot[1]

    #copy the dictionary. One copy will be manipulated for Mentioned, the other for NotMentioned
    weekToSongListCopy=copy.deepcopy(weekToSongList)

    ###MENTIONED CODE
    #take mentioned songs and all songs and get the intersection of the two sets
    mentionedWeekToSongList=genNewWeekToSongList(Mentioned,weekToSongList)
    #calculate the avg sentiment score for the intersection
    AvgMentLabel=getAvg(weekToSongList,dictionary)

    ##NOT MENTIONED CODE
    #take not mentioned songs and all songs and get the intersection of the two sets
    genNewWeekToSongList(NotMentioned,weekToSongListCopy)
    #calculate the avg sentiment score for the intersection
    AvgNotLabel=getAvg(weekToSongListCopy,dictionary)

    #iterating over dictionary keys is random in order
    #so sort tuples (key, value) based on key order
    AvgSongLabel=sorted(AvgSongLabel,key=lambda x: x[0])
    AvgMentLabel=sorted(AvgMentLabel,key=lambda x: x[0])
    AvgNotLabel=sorted(AvgNotLabel,key=lambda x: x[0])

    #strip tuples of key number since values are now sorted
    #Subset to week 16:. More reliable data. See stacked bar chart; early months had lowest mentions.
    AvgSongLabel=[i[1] for i in AvgSongLabel][16:]
    AvgMentLabel=[i[1] for i in AvgMentLabel][16:]
    AvgNotLabel=[i[1] for i in AvgNotLabel][16:]
    WeekLabel=WeekLabel[16:]

    #use lists of labels and data to create plot
    plot(WeekLabel,AvgSongLabel,AvgMentLabel,AvgNotLabel)

if __name__ == "__main__": 
    main()