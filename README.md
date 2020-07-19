# AirOvalCode

## About Me 
Hello, I'm Paige and I'm interested in Data Science! As I have an MSc in Climate Science, I thought I would set up a hobby project to monitor particulate matter (PM) concentrations in my local area. This project has lead me to learn a lot more about Data Science! 

## About the Project
I have used a SDS011 home air quality sensor, to measure PM 2.5 and PM 10 concentrations down a quiet road in the Oval neighbourhood of London. I have used a Raspberry Pi to read data from the sensor. A reading is taken every minute. Throughout this project, I have used Python3, Jupyter NoteBook and Lab, and matplotlib. At first, my data was written to a CSV file and later to a MySQL instance in the AWS cloud. 

## @AirOval Twitter Account 
To share my project, I created a Twitter developer account where I publish visualisations of my data in the form of graphs and gauges, and post and re-tweet information about air quality. You can find my account here: [link](https://twitter.com/AirOval)

So far, these are the visualisations which I've created:

* A Daily Graph: This graph is automatically published every day at 3am, and shows the moving average of the PM concentrations over the last 24 hours (midnight - midnight). 
* A Weekly Graph: This graph is automatically published every Monday at 4am, and shows all the data points over a week, as well as the moving average. 

The code for these graphs can be viewed in graph_maker.py 

* A PM Concentration Index: This has yet to be automated, but the gauge visualises the severity of PM concentration. 

The code for the gauge can be viewed in gauge.py 

I have also published the code which reads data from the sensor, and saves the data to a CSV file and the MySQL database. This can be viewed in home_air_qual_data.py




