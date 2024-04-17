import pandas as pd
import numpy as np

def main():

    with open("financialData.csv", "r") as file:
        df = pd.read_csv(file)
    
    with open("Tickers.csv", "r") as file:
        stocks = pd.read_csv(file)

    with open("masterDataframe.csv", "r") as file:
        top100 = pd.read_csv(file)
    
    with open("SongsTickerMentions.csv", "r") as file:
        song = pd.read_csv(file)

    #Dictionary for industry mapping
    
    industryDict = {"QSR":"foodservice","RACE":"automobile","RL":"clothing","GOOS":"clothing", 
    "KORS":"accessories","MAR":"hospitality","MCD":"foodservice","YUM":"foodservice",
    "TIF":"accessories","LUX":"accessories","PVH":"clothing","MOV":"accessories",
    "EL":"cosmetics","PRDSY":"accessories","POAHY":"automobile","VFC":"clothing",
    "JWN":"clothing","BGI":"accessories","M":"department","NKE":"sports",
    "GPS":"clothing","HBI":"clothing","UA":"sports","BOSS":"clothing",
    "ADS":"sports","LULU":"sports","PUMA":"sports","FL":"footwear",
    "SKX":"footwear","URBN":"clothing","AEO":"clothing","DKS":"sports",
    "SHOO":"accessories","ANF":"clothing","JCP":"department","VRA":"accessories",
    "FOSL":"accessories","TJX":"department","LB":"clothing","VIPS":"ecommerce",
    "CRI":"accessories","COLM":"sports","DECK":"outdoor","WWW":"footwear",
    "DDS":"department","OXM":"clothing","GES":"clothing","CAL":"footwear",
    "CHS":"clothing","BKE":"clothing","GCO":"footwear","EXPR":"clothing",
    "FRAN":"clothing","JCG":"clothing","ZUMZ":"footwear","SIG":"accessories",
    "SWGAY":"accessories","YETI":"outdoor","F":"automobile","GM":"automobile",
    "CMG":"foodservice","AUDVF":"automobile","TM":"automobile","AAPL":"electronics",
    "HMC":"automobile","AMZN":"department"}


    #Make our binary var column 8
    df['Increase_This_Week'] = df.apply(lambda row: increase(row), axis=1)
    #Make percent increase var column 9
    df['Delta_Price'] = df.apply(lambda row: percentIncrease(row), axis=1)
    #Log transform volume becasue Apple and Ford have volumes in the billions
    #Column 10
    df["log_volume"] = df.apply(lambda row: logTransform(row, "volume"), axis=1)
    
    songMentions(df, top100, song)
    
    industry(df, industryDict)
    countIndustry(df)
    consecutive(df)
    #print(df)
    with open("FullData.csv", "w") as dataFile:
        df.to_csv(dataFile, encoding='utf-8', index=False)


#Get number of song mentions, unique mentions, and list of artists
def songMentions(df, top100, song):
    ment = pd.DataFrame(columns=["num_mentions"])
    uniq = pd.DataFrame(columns=["unique_songs"])
    artist = pd.DataFrame(columns=["artist_mentions"])
    #For each row in the data frame
    for i in range(0, len(df),1):
        print("Processing: " , df['ticker'][i])
        sub = top100.loc[top100['Dates']==df['date'][i]] #get the top100 lookup for that ticker
        mentions =0
        uniques = 0
        arts = []
        for title in sub["Song"]: #For every song title
            if(fetch(song, title, df["ticker"][i])>0):
                mentions += fetch(song, title, df["ticker"][i]) #Fetch the number of times the stock is mentioned
                uniques += 1
                arts.append(fetchArt(song, title)) #Fetch the artists
        ment= ment.append({'num_mentions': mentions}, ignore_index=True)
        uniq= uniq.append({'unique_songs': uniques}, ignore_index=True)
        artist = artist.append({'artist_mentions': arts}, ignore_index=True)
    #Add new df values to the super dataframe
    df["num_mentions"] = ment["num_mentions"].values
    df["unique_songs"] = uniq["unique_songs"].values
    df["artist_mentions"] = artist["artist_mentions"].values

#Perform lookup using industry Dictionary to map ticker to industry
def industry(df, industryDict):
    indust = pd.DataFrame(columns=["industry"])
    for i in range(0 , len(df), 1):
        indust = indust.append({"industry": industryDict[df["ticker"][i]]}, ignore_index=True)
    df["industry"] = indust["industry"].values

#Count the total number of times each industry is mentioned over the entire year
def countIndustry(df):
    df["industry_mentions"] = 0
    vals = ["foodservice", "automobile", "clothing", "accessories", "hospitality", "cosmetics", "department", "sports", "footwear", "ecommerce", "outdoor", "electronics"]
    industcount = pd.DataFrame(columns=["industry_mentions"])
    for val in vals: #For each industry
        count = 0
        hold = df.loc[df["industry"]==val] #get the set of the dataframe of that industry
        for mentions in hold["num_mentions"]:   
            count+=mentions #add total number of mentions
        df.loc[df["industry"]==val, "industry_mentions"] = count


def fetchArt(song, title):
    #Song returns as series so we convert to df
    hold = song.loc[song["Song"]==title]
    df = hold["Artist"].to_frame()
    df.columns = ["art"]
    arts = df["art"].tolist()
    final = ""
    for name in arts:
        #catch dirty data from scraping
        dirt = name.split(" Lyrics")
        final += dirt[0] +","
    return final

#fetch the number of times a stock was mentioned for a given song
def fetch(song, title, ticker):
    hold = song.loc[song["Song"]==title]
    if hold.empty ==False:
        x = int(hold[ticker])
        return x
    else:
        return 0

def consecutive(df):
    df["consecutive_weeks"] = 0
    for j in range(0 , len(df), 1):
        if j==0: #Base case for first row
            df["consecutive_weeks"] = 0
        else:
            if(df["ticker"][j-1]==df["ticker"][j]): #if the row before it has the same ticker
                if df["num_mentions"][j-1]>0: #if it is mentioned this week
                    df["consecutive_weeks"][j] =int(df["consecutive_weeks"][j-1]+1)
                else: #otherwise reset consecutive weeks
                    df["consecutive_weeks"][j] = 0
            else: #if its a new stock set it to 0
                df["consecutive_weeks"][j] = 0
    

#Gets the change in price for the week, meant to be used as lambda function
def increase(row):
    if row['close']-row['open']>0:
        return 1
    else:
        return 0  

#lambda function for getting percent change in price per week
def percentIncrease(row):
      return 100*((row['close']-row['open'])/row['open'])

#log transform whatever row we want, I used it to log transform the volume 
def logTransform(row, header):
    if(row[header]!=0):
      return np.log(row[header])
    return 0

if __name__ == "__main__":
    main()