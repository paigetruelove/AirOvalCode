# Importing API keys from Twitter - API keys let you into the Twitter account without need of password 
from twython import Twython
from auth import (
    consumer_key,
    consumer_secret,
    access_token,
    access_token_secret
)

import gauge_maker
import random # Importing the Random module to randomise the daily Twitter messages 
import graph_maker # Importing the file "graph_maker" where the fuction "create_graph" can be found 
import sys

days = int(sys.argv[1]) # Reads in the second element of data which has been specified in the command line 
print("Working over " + str(days) + " days")
graph_maker.getdata(days)

print("Composing Tweet")
twitter = Twython(
    consumer_key,
    consumer_secret,
    access_token,
    access_token_secret
)

if (days == 1):
    # Writing the text for the daily Tweet 
    messages = ["Yesterday's PM stats!",
                "Check out yesterday's PM levels!",
                "Another day, another graph!",
                "Good Morning! Here's your daily graph:"]
    message = random.choice(messages)
    
    # Opening image of daily graph 
    image = open('dailymagraph.png', 'rb')
    
    # Uploading daily graph to Twitter 
    response = twitter.upload_media(media=image)
    graph_id = [response['media_id']]
    
    # Creating image of daily gauge 
    gauge_maker.create_daily_gauge()
    image = open('pmConcentrationIndex.png', 'rb')
    
    # Uploading daily gauge to Twitter
    response = twitter.upload_media(media=image)
    gauge_id = [response['media_id']]
    
    media_id = graph_id + gauge_id
    
if (days == 7):
    # Writing the text for the weekly Tweet 
    messages = ["Good Morning! Here's last week's PM stats!",
                "Another week, another weekly graph!",
                "Happy Monday! Here's your weekly graph:"]
    message = random.choice(messages)
    
    # Opening image of weekly graph 
    image = open('weeklygraphwithma.png', 'rb')
    
    # Uploading weekly graph to Twitter 
    response = twitter.upload_media(media=image)
    media_id = [response['media_id']]

print(message)

# Sending Tweet 
twitter.update_status(status=message, media_ids=media_id)

print("Tweeted Sucessfully")