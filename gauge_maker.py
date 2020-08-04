import pandas as pd
from matplotlib import pyplot as plt
import datetime
import matplotlib.dates as mdates
import pm_gauge

def create_daily_gauge():
    plt.style.use('dark_background')

    publishData = pd.read_csv("~/Desktop/home_air_qual_publishdata.csv", parse_dates=["datetime"])

    # Removing any sensor errors i.e. readings greater than 100 
    publishData = publishData[publishData["pmten"] <100]
    publishData = publishData[publishData["pmtwofive"] <100]

    # Calculating the quartiles (20%, 40%... etc.)
    q10 = publishData.quantile(q=0.10)
    q25 = publishData.quantile(q=0.25)
    q75 = publishData.quantile(q=0.75)
    q90 = publishData.quantile(q=0.90)

    # Getting yesterday's data (midnight - midnight)
    midnight = datetime.time(0,0,0)
    startdate = datetime.datetime.now() - datetime.timedelta(days=1)
    windowstart = datetime.datetime.combine(startdate.date(), midnight)
    windowend = windowstart + datetime.timedelta(days=1)

    plotPublishData = publishData[publishData["datetime"] > windowstart]
    plotPublishData = plotPublishData[plotPublishData["datetime"] < windowend]

    # Calculates the mean for yesterday's data 
    dailyMean = plotPublishData.mean()

    # Logic behind where the arrow points on each PM gauge
    if dailyMean["pmten"] < q10["pmten"]: 
        arrow1 = 1 
    elif dailyMean["pmten"] < q25["pmten"]:
        arrow1 = 2
    elif dailyMean["pmten"] < q75["pmten"]: 
        arrow1 = 3
    elif dailyMean["pmten"] < q90["pmten"]:
        arrow1 = 4
    else:
        arrow1 = 5

    if dailyMean["pmtwofive"] < q10["pmtwofive"]: 
        arrow2 = 1 
    elif dailyMean["pmtwofive"] < q25["pmtwofive"]:
        arrow2 = 2
    elif dailyMean["pmtwofive"] < q75["pmtwofive"]: 
        arrow2 = 3
    elif dailyMean["pmtwofive"] < q90["pmtwofive"]:
        arrow2 = 4
    else:
        arrow2 = 5

    # Produces the gauge image    
    pm_gauge.gauge(arrow1=arrow1, arrow2=arrow2)