import pandas as pd
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
import datetime
import matplotlib.dates as mdates

def getdata(daysToGet):
    """ 
    This function imports the CSV file which contains the sensor data, and selects a specified data timeframe to create a graph. 
    daysToGet -- This argument specifies the number of days to retrieve data (i.e 1 would get you yesterdays data). 
    The timeframe has been specified as being midnight to midnight (i.e. 0,0,0). 
    """

    # Importing the CSV file which contains the PM data 
    print(datetime.datetime.now())
    print("Importing CSV")
    publishData = pd.read_csv("~/Desktop/home_air_qual_publishdata.csv", parse_dates=["datetime"])

    # Sense check - making sure any data which is over 100 is dropped (to avoid publishing/Tweeting sensor errors etc.)
    publishData = publishData[publishData["pmten"] <100]
    publishData = publishData[publishData["pmtwofive"] <100]
    

    # Gets the data from the specified time window i.e. how many days back you want to go (e.g. 1 or 7)
    print("Calculating dates")
    midnight = datetime.time(0,0,0)
    startdate = datetime.datetime.now() - datetime.timedelta(days=daysToGet)
    windowstart = datetime.datetime.combine(startdate.date(), midnight)
    windowend = windowstart + datetime.timedelta(days=daysToGet)

    plotPublishData = publishData[publishData["datetime"] > windowstart]
    plotPublishData = plotPublishData[plotPublishData["datetime"] < windowend]
    
    # Creates graph based on yesterdays days (i.e 1 day ago)
    if (daysToGet == 1):
        createdailygraph(windowstart, plotPublishData)
    # Creates graph based on the last week of data (i.e 7 days ago)
    if (daysToGet == 7):
        createweeklygraph(windowstart, windowend, plotPublishData)

        
def createdailygraph(windowstart, plotDailyData):
    """ 
    This function creates a daily graph using yesterday's recorded data.
    windowstart -- This argument is the beginning of the timeframe.
    plotDailyData -- This is the dataframe to be plotted. 
    """
    
    # States which style to plot graphs in 
    plt.style.use('dark_background')
                  
    print("Creating plot")
    fig, ax = plt.subplots(2)
    fig.suptitle("Moving Average (MA) Daily Particulate Matter Concentration: " + windowstart.strftime("%d/%m/%Y"))
    
    # Specifying how many points the moving average (ma) moves in 
    ma = 50

    plotDailyData = plotDailyData.set_index(pd.DatetimeIndex(plotDailyData["datetime"]))

    # Subgraph 1 (PM 10 Graph)
    ax[0].plot(plotDailyData.index, plotDailyData["pmten"].rolling(ma).mean(), color="orange")

    # Adding/Manipulating graph labels
    ax[0].set(ylabel="µg/m3")
    ax[0].axes.xaxis.set_ticklabels([]) # This hides the x labels on the first graph to avoid overlapping
    ax[0].legend(["PM 10", "PM 10 MA"], bbox_to_anchor=(1.3, 0.5))

    # Subgraph 2 (PM 2.5 Graph)
    ax[1].plot(plotDailyData.index, plotDailyData["pmtwofive"].rolling(ma).mean(), color="lightblue")
    
    # Adding/manipulating graph labels
    ax[1].xaxis.set_major_formatter(mdates.DateFormatter('%H:00')) # Formatting the x label to show hours in 24 hour format
    ax[1].set(xlabel="Hour (24)", ylabel="µg/m3")
    labels1 = ax[1].get_xticklabels()
    plt.setp(labels1, rotation=45, horizontalalignment='right')
    ax[1].legend(["PM 2.5", "PM 2.5 MA"], bbox_to_anchor=(1.3, 0.5))
    
    # Saving a png file of the graph 
    fig.savefig("dailymagraph.png", dpi=200, bbox_inches="tight")


def createweeklygraph(windowstart, windowend, plotWeeklyData):
    """
    This function creates a weekly graph using the previous week's recorded data.
    windowstart -- This argument is the beginning of the timeframe.
    windowend -- This argument is the end of the timeframe.
    plotWeeklyData -- This is the dataframe to be plotted.
    """
    
    # States which style to plot graphs in 
    plt.style.use('dark_background')
    
    fig, ax = plt.subplots(2)
    fig.suptitle("Moving Average (MA) Weekly Particulate Matter Concentration: " + windowstart.strftime("%d/%m/%Y - ") + windowend.strftime("%d/%m/%Y"))
    
    # Specifying how many points the moving average (ma) moves in
    ma = 200
    
    plotWeeklyData = plotWeeklyData.set_index(pd.DatetimeIndex(plotWeeklyData["datetime"]))
    
    # Subgraph 1 (PM 10 Graph)
    ax[0].plot(plotWeeklyData.index, plotWeeklyData["pmten"], color="orange", alpha=0.7)
    ax[0].plot(plotWeeklyData.index, plotWeeklyData["pmten"].rolling(ma).mean(), color="white")

    # Adding/manipulating graph labels
    ax[0].set(ylabel="µg/m3")
    ax[0].axes.xaxis.set_ticklabels([]) # This hides the x labels on the first graph to avoid overlapping
    ax[0].legend(["PM 10", "PM 10 MA"], bbox_to_anchor=(1.3, 0.5))

    # Subgraph 2 (PM 2.5 Graph)
    ax[1].plot(plotWeeklyData.index, plotWeeklyData["pmtwofive"], color="lightblue", alpha=0.7)
    ax[1].plot(plotWeeklyData.index, plotWeeklyData["pmtwofive"].rolling(ma).mean(), color="white")

    # Adding/manipulating graph labels
    ax[1].set(xlabel="Day", ylabel="µg/m3")
    labels1 = ax[1].get_xticklabels()
    ax[1].xaxis.set_major_formatter(mdates.DateFormatter('%a')) # Formating date to show day in abbreviated  format (i.e. Mon, Tue...)
    plt.setp(labels1, rotation=45, horizontalalignment='right')
    ax[1].legend(["PM 2.5", "PM 2.5 MA"], bbox_to_anchor=(1.3, 0.5))

    # Saving a png file of the graph
    fig.savefig("weeklygraphwithma.png", dpi=200, bbox_inches="tight")