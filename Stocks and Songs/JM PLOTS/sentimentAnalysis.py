import pandas as pd
from pprint import pprint
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer
import nltk
import chart_studio.plotly as py
import plotly.graph_objs as go
import plotly.express as px
import numpy as np
import matplotlib.pyplot as plt
import chart_studio
import chart_studio.plotly as py

def main():
    myDataFrame = getData() #reads in data to data frame from csv
    myDataFrame = findPolarity(myDataFrame) #finds polarity of each song based on lyrics
    myScatterData = createTrace(myDataFrame) #creates trace - defining x and y variables
    myLayout = layout() #creates layout of scatterplot
    myScatterDisplay = setup(myScatterData,myLayout) #creates scatterplot with given data and layout

    # username = 'jam580'
    # api_key = 'N0vDnbORLSc0eGxH7Gzg'

    # chart_studio.tools.set_credentials_file(username=username, api_key=api_key)
    # py.plot(myScatterData, filename = 'Sentiment', auto_open=True)

    myScatterDisplay.show() #shows figure
    myDataFrame.to_csv("polarity.csv") #creates a csv of data frame with sentiment scores
    polarityDict = makeDict() #makes a dictionary of manually labelled polarities for 21 songs
    sentimentDf = outputManualSentiment(myDataFrame,polarityDict) #creates a dataframe of 21 songs and their TextBlob sentiment scores and manually generated sentiment scores
    makeBargraph(sentimentDf) #makes a bargraph from sentiment dataframe

def getData(): #reads in data to data frame from csv
    myDataFrame = pd.read_csv("Tokenized LyricsCSV.csv", sep = ",")
    return myDataFrame

def findPolarity(myDataFrame): #finds polarity of each song based on lyrics
    myDataFrame.insert(5,"testimonial",0) #inserts a new column called "testimonial"
    myDataFrame.insert(6,"polarity",0) #inserts a new column called "polarity"
    for index, row in myDataFrame.iterrows(): #loops through each row
        myDataFrame["testimonial"][index] = TextBlob(myDataFrame["Lyrics"][index]) #tokenizes lyrics for each song
    polarityList = [] #creates empty list
    for index, row in myDataFrame.iterrows(): #loops through each row
        polarityList.append((myDataFrame["testimonial"][index]).sentiment.polarity) #uses sentiment analysis to find polarity of string of tokenized lyrics
    myDataFrame["polarity"] = polarityList #adds list of polarities to data frame
    myDataFrame = myDataFrame.sort_values(by=["polarity"])
    return myDataFrame

def createTrace(dataFrame): #creates trace - defining x and y variables
    trace = go.Scatter(
	    x = dataFrame['Song'], #defines x variable
	    y = dataFrame['polarity'], #defines y variable
	    mode = 'markers'
    )
    myData = [trace]
    return myData

def layout(): #creates layout of scatterplot
    #labels title and axes
    myLayout = go.Layout(title = "Polarity of Song Lyrics",xaxis=dict(title = 'Song'),yaxis=dict(title = 'Polarity'))
    return myLayout

def setup(data,layout): #creates scatterplot with given data and layout
    myFigure = go.Figure(data=data, layout=layout)
    return myFigure

def makeDict(): #makes a dictionary of manually labelled polarities for 21 songs
    polarityDict = {"happens":0,"every":0,"time":0,"sounds":0,"like":0,"suicide":-1,
    "hesitant":-0.7,"drink":0,"kool":0,"yeah":0,"thought":0,"life":0,
    "whoa":0,"look":0,"mind":0,"better":0.3,"place":0,"align":0,"universe":0,
    "must":0,"back":0,"fell":-0.2,"youre":0,"soulmate":0.6,"whole":0,"ready":0,
    "happy":0.7,"wont":-0.4,"beautiful":0.9,"angel":0.9,"love":1,"angle":0,
    "tomorrow":0,"comes":0,"goes":0,"know":0,"gucci":0,"amazing":0.9,"nothing":-0.4,
    "compare":0,"naked":0,"backwood":0,"henny":0,"faded":0,"saying":0,"need":0,
    "face":0,"started":0,"younger":0,"swear":-0.1,"loved":1,"sorry":-0.7,"found":0,
    "guess":0,"really":0,"thunder":-0.2,"aint":-0.4,"nobody":-0.2,
    "imperfections":-0.7,"dress":0,"miracle":1,"creation":0.1,"little":0,"taste":0,
    "shaking":0,"never":-0.9,"ever":0,"mislead":-0.7,"believe":0,"lies":-0.8,"feed":0,
    "stop":-0.6,"stare":0,"sculpture":0,"painted":0,"colors":0.1,"sometimes":0,"shine":0.4,
    "hate":-1,"froze":0,"niggas":-1,"nigga":-1,"hoes":-0.8,"watching":0,"outside":0,"sauce":0,"fuck":-1,
    "verified":0,"thottie":-0.2,"wife":0,"playin":0,"kitty":0,"beat":-0.3,"shawty":0.2,
    "swallow":0,"meat":0,"smoked":0,"fire":-0.6,"lung":0,"dope":0.7,"sock":0,"want":0,
    "rock":0,"pull":0,"babe":0.6,"kiss":0.6,"slowly":0,"sweetest":1,"thing":0,"change":0,
    "coffee":0,"morning":0,"sunshine":0.8,"rain":-0.3,"pouring":-0.3,"give":0,"star":0.5,
    "follow":0,"matter":0,"movie":0,"brown":0,"eyes":0,"desire":0.4,"wake":0,"nice":0.6,
    "water":0,"stuck":-0.7,"desert":0,"tylenol":0,"take":0,"head":0,"hurts":0.8,"traveling":0,
    "packs":0,"cant":-0.4,"carry":0,"anymore":0,"waiting":-0.2,"somebody":0,"else":0,"door":0,
    "people":0,"arent":-0.4,"used":0,"tried":0,"save":0.2,"saturday":0,"repent":0,"mama":0,
    "another":0,"amen":0,"couldnt":-0.4,"sleep":0,"gave":0,"everything":0,"beside":0,"said":0,
    "pray":0.5,"wicked":-1,"weekend":0,"sick":-0.8,"hire":0,"help":0,"shit":-0.8,"move":0,
    "ritz":0,"turned":0,"bitch":-1,"lambo":0,"movin":0,"fast":0,"class":0,"lotta":0,
    "rocket":0,"tags":0,"louis":0,"bags":0,"exchange":0,"body":0,"whatever":-0.4,"tired":-0.3,
    "knock":0,"tithes":0,"gone":-0.7,"dont":-0.4,"lovey":1,"dovey":0,"brother":0,"late":-0.4,
    "prada":0,"shook":0,"please":0,"fool":-0.6,"care":0,"quiet":0,"shush":-0.2,"comin":0,
    "edge":0,"cook":0,"lead":0,"league":0,"scorin":0,"assists":0,"future":0,
    "reminisce":0.4,"forget":-0.4,"patient":0.5,"gift":0.8,"tell":0,"insist":0,"million":0,
    "chappelle":0,"standing":0,"coffin":-1,"hammer":0,"nail":0,"heard":0,"name":0,"ring":0,
    "bell":0,"everyone":0,"knew":0,"deserts":0,"fight":-0.8,"facin":0,"dark":-0.8,
    "hall":0,"grab":0,"light":0.8,"surrounded":0,"wall":0,"shred":0,"choices":0,
    "defend":0,"blood":0.7,"lions":0,"jump":0,"party":0.7,"ride":0,"live":0,
    "welcome":0,"dogs":0,"ridin":0,"high":0,"coupe":0,"ceilin":0,"rocks":0,"watch":0,
    "armageddon":0,"roof":0,"tank":0,"ciroc":0,"drop":0,"full":0,"beans":0,"squad":0,"cars":0,
    "burn":-0.6,"riot":-0.6,"crack":-0.2,"rich":0.6,"probation":-0.7,"hatin":-1,"attack":-0.8,
    "stressed":-0.7,"lost":-0.5,"heartbreaking":-1,"bitches":-1,"shady":-0.6,
    "begging":-0.4,"shoot":-0.4,"dumb":-0.8,"damage":-0.8,"fucking":-1,"easy":0.3,"heaven":1,
    "darling":0.5,"passion":0.9,"smile":0.8,"wonderland":1,"dreamer":0.3,"fucked":-1,"jail":-0.8,
    "hurt":-0.8,"worse":-0.7,"hell":-1,"lucifer":-1,"stupider":-0.8,"abusin":-0.9,"coward":-0.8,
    "homie":0.6,"noose":-0.7,"died":-0.9,"evil":-1,"freedom":0.7,"drugs":-0.3,"freeze":-0.2,
    "bleed":-0.7,"ambulance":-0.6,"nightmare":-1,"slaves":-1,"killed":-1,"kill":-1,"bullet":-0.4,
    "fail":-1,"shackles":-0.5,"felon":-0.9,"rains":-0.3,"pours":-0.3,"temptations":-0.6,
    "decline":-0.2,"strong":0.3,"loving":1,"crime":-0.8,"creep":-0.8,"fake":-0.5,"fears":-0.4,
    "selfish":-0.6,"bruise":-0.2,"confusin":-0.1,"addict":-0.5,"lames":-0.5,"lame":-0.5,
    "shame":-0.6,"fuckin":-1,"crash":-0.4,"safe":0.3,"birthday":0.4,"broke":-0.7,
    "curse":-0.9,"passionate":0.9,"baby":0.6,"harm":-0.8,"good":0.5,"emergency":-1,"broken":-0.7,
    "lonely":-0.8,"juvie":-0.8,"lose":-0.5,"damn":-0.3,"intimidatin":-0.4,"creepin":-0.8,
    "problems":-0.8,"pussy":-0.3,"besties":0.8,"messy":-0.5,"crazy":-0.5,"madness":-0.5,
    "burning":-0.6,"choked":-0.7,"goodbye":-0.4}
    return polarityDict

def selfPolarity(myDataFrame, dict,x,list): #calculates sentiment score and appends that score to a list
    #formats Tokenized_Lyrics into a string
    myString = str(myDataFrame["Tokenized_Lyrics"][x])
    myString = myString.replace("'", '')
    myString = myString.replace(",",'')
    sum = 0
    for word in myString.split():
        if (word in dict): #checks if word in lyrics exists in manually created dictionary
            sum += dict.get(word) #if yes, add corresponding polarity to total
    length = len(myString.split()) #computes how many words in each song lyric
    score = sum/length #calculate sentiment score by averaging polarities
    list.append(score) #appends score to the list
    return list

def outputManualSentiment(myDataFrame, polarityDict): #creates a dataframe of 21 songs and their TextBlob sentiment scores and manually generated sentiment scores
    scoreList = [] #creates empty list that will keep track of manually generated sentiment scores
    #each selfPolarity function call will append the sentiment score of that song to the list
    #Pete Davidson
    scoreList = selfPolarity(myDataFrame,polarityDict,278,scoreList) 
    #Jonestown
    scoreList = selfPolarity(myDataFrame,polarityDict,187,scoreList)
    #Beautiful
    scoreList = selfPolarity(myDataFrame,polarityDict,36,scoreList)
    #I don't Let Go
    scoreList = selfPolarity(myDataFrame,polarityDict,171,scoreList)
    #Best Part
    scoreList = selfPolarity(myDataFrame,polarityDict,40,scoreList)
    #Mob Ties
    scoreList = selfPolarity(myDataFrame,polarityDict,233,scoreList)
    #Say Amen (Saturday Night)
    scoreList = selfPolarity(myDataFrame,polarityDict,305,scoreList)
    #My Blood
    scoreList = selfPolarity(myDataFrame,polarityDict,187,scoreList)
    #Welcome To The Party
    scoreList = selfPolarity(myDataFrame,polarityDict,383,scoreList)
    #WAKA
    scoreList = selfPolarity(myDataFrame,polarityDict,369,scoreList)
    #One Kiss
    scoreList = selfPolarity(myDataFrame,polarityDict,264,scoreList)
    #Trauma
    scoreList = selfPolarity(myDataFrame,polarityDict,359,scoreList)
    #Born to be Yours
    scoreList = selfPolarity(myDataFrame,polarityDict,52,scoreList)
    #Kevin's Heart
    scoreList = selfPolarity(myDataFrame,polarityDict,193,scoreList)
    #Big Bank
    scoreList = selfPolarity(myDataFrame,polarityDict,44,scoreList)
    #Arms Around You
    scoreList = selfPolarity(myDataFrame,polarityDict,22,scoreList)
    #A Girl like You
    scoreList = selfPolarity(myDataFrame,polarityDict,12,scoreList)
    #Coming Home
    scoreList = selfPolarity(myDataFrame,polarityDict,78,scoreList)
    #Broken
    scoreList = selfPolarity(myDataFrame,polarityDict,54,scoreList)
    #LOSE IT
    scoreList = selfPolarity(myDataFrame,polarityDict,197,scoreList)
    #Always Remember Us This Way
    scoreList = selfPolarity(myDataFrame,polarityDict,21,scoreList)
    #creates sentimentDf of each of our chosen songs and their corresponding sentiment score calculated by TextBlob
    songs = {"Song":["Pete Davidson","Jonestown","Beautiful","I Don't Let Go","Best Part","Mob Ties",
    "Say Amen (Saturday Night)","My Blood","Welcome To The Party","WAKA","One Kiss","Trauma","Born To Be Yours",
    "Kevin's Heart","Big Bank","Arms Around You","A Girl Like You","Coming Home","Broken","LOSE IT","Always Remember Us This Way"],
    "Sentiment Score":[myDataFrame["polarity"][278],myDataFrame["polarity"][187],myDataFrame["polarity"][36],myDataFrame["polarity"][171],
    myDataFrame["polarity"][40],myDataFrame["polarity"][233],myDataFrame["polarity"][305],myDataFrame["polarity"][187],myDataFrame["polarity"][383],
    myDataFrame["polarity"][369],myDataFrame["polarity"][264],myDataFrame["polarity"][359],myDataFrame["polarity"][52],myDataFrame["polarity"][193],
    myDataFrame["polarity"][44],myDataFrame["polarity"][22],myDataFrame["polarity"][12],myDataFrame["polarity"][78],myDataFrame["polarity"][54],
    myDataFrame["polarity"][197],myDataFrame["polarity"][21]]}
    sentimentDf = pd.DataFrame(songs)
    sentimentDf.insert(2,"Manually Generated Sentiment",scoreList) #inserts our manually generated sentiment score to sentimentDf
    return sentimentDf

def makeBargraph(dataFrame): #makes a bargraph from sentiment dataframe
    dataFrame = dataFrame.sort_values(by="Sentiment Score") #sort sentiment scores by ascending value
    fig, ax =  plt.subplots() #create subplot
    numGroups = 21 #number of songs
    index = np.arange(numGroups) #creates evenly spaced values
    barWidth = 0.35
    opacity = 0.8
    regScore = plt.bar(index,dataFrame["Sentiment Score"],barWidth,alpha=opacity,color="b",label="TextBlog Library") #creates bar from TextBlob's scores
    selfScore = plt.bar(index+barWidth,dataFrame["Manually Generated Sentiment"],barWidth,alpha=opacity,color="g",label="Manually Generated") #creates bar from manual scores
    #labels axes and title
    plt.xlabel("Song")
    plt.ylabel("Sentiment Score")
    plt.title("Sentiment Score by Text Blob Library vs. Manually Generated")
    plt.xticks(index + barWidth,dataFrame["Song"], rotation = 'vertical')
    plt.legend()
    plt.rcParams.update({'font.size':22})
    plt.tight_layout()
    plt.show()

main()