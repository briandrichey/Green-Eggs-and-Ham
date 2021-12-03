# regex library
import regex

import astral

#from astropy.coordinates import get_sun, AltAz, EarthLocation
#from astropy.time import Time
#import astropy as ast
#import astropy.units as u
#from astropy.time import Time
#from astropy.coordinates import SkyCoord, EarthLocation, AltAz

# scikit libraries
from sklearn import preprocessing
import numpy as np

# matplotlib libraries
from matplotlib import pyplot as plt

# upload libraries to clean data with commas
from pathlib import Path
import os
import sys

# upload libraries for pandas
import pandas as pd

# upload libraries for timing the processing time
import time

import datetime
from timezonefinder import TimezoneFinder
import pytz

import math

###########################################################
# function that will process a line by                    #
# separating its components with commas                   #
#                                                         #
# li is the current line of data that is being processed. #
###########################################################
def sunpos(when, location):
    # Extract the passed data
    year, month, day, hour, minute, second = when
    latitude, longitude = location

    tf = TimezoneFinder()

    # From the lat/long, get the tz-database-style time zone name (e.g. 'America/Vancouver') or None
    timezone_str = tf.timezone_at(lng = longitude, lat = latitude)
    timezone = pytz.timezone(timezone_str).localize(datetime.datetime(year, day, month)).strftime("%z")

    # Math typing shortcuts
    rad, deg = math.radians, math.degrees
    sin, cos, tan = math.sin, math.cos, math.tan
    asin, atan2 = math.asin, math.atan2
    # Convert latitude and longitude to radians
    rlat = rad(latitude)
    rlon = rad(longitude)
    # Decimal hour of the day at Greenwich '''- timezone ''' (betw hour and min)
    locationtime = hour - int(timezone) + minute / 60 + second / 3600
    # Days from J2000, accurate from 1901 to 2099
    daynum = (367 * year - 7 * (year + (month + 9) // 12) // 4 + 275 * month // 9 + day - 730531.5 + locationtime / 24)
    # Mean longitude of the sun
    mean_long = daynum * 0.01720279239 + 4.894967873
    # Mean anomaly of the Sun
    mean_anom = daynum * 0.01720197034 + 6.240040768
    # Ecliptic longitude of the sun
    eclip_long = (mean_long + 0.03342305518 * sin(mean_anom) + 0.0003490658504 * sin(2 * mean_anom))
    # Obliquity of the ecliptic
    obliquity = 0.4090877234 - 0.000000006981317008 * daynum
    # Right ascension of the sun
    rasc = atan2(cos(obliquity) * sin(eclip_long), cos(eclip_long))
    # Declination of the sun
    decl = asin(sin(obliquity) * sin(eclip_long))
    # Local sidereal time
    sidereal = 4.894961213 + 6.300388099 * daynum + rlon
    # Hour angle of the sun
    hour_ang = sidereal - rasc
    # Local elevation of the sun
    elevation = asin(sin(decl) * sin(rlat) + cos(decl) * cos(rlat) * cos(hour_ang))
    # Local azimuth of the sun
    azimuth = atan2(-cos(decl) * cos(rlat) * sin(hour_ang), sin(decl) - sin(rlat) * sin(elevation),)
    
    # Convert azimuth and elevation to degrees
    azimuth = deg(azimuth) % 360 #, 0, 360)
    elevation = deg(elevation) #, -180, 180)
    # make sure that the range of the elevation is between -180 and 180
    if elevation > 180: elevation = elevation - 360

    # Return azimuth and elevation in degrees
    return (round(azimuth, 2)), (round(elevation, 2))


###########################################################
# function that will process a line by                    #
# separating its components with commas                   #
#                                                         #
# li is the current line of data that is being processed. #
###########################################################
def process(li):
    #get the location prefix codes from the excel file
    locDf = pd.read_excel("CallSignSeriesRanges.xlsx")
    locDf.columns = [ "series", "series_prefix", "location" ]
    #print(locDf)

    #split the data and store its peices into a data list
    dataList = li.split()

    #the list that will hold the processed data
    processedLineList = []
    #the list that will hold callsigns
    callsigns = ""

    #indicates whether there is a message or not in the line of data
    messageExists = False
    #get the last piece of data of the line of data to determine whether this is a message or not
    lastDataPiece = dataList[len(dataList) - 1]
    #indicates what type of message the last piece of data is if it is a message
    messageType = ""
    #counts how many callsigns are within a line of data
    callsignCounter = 0
    #indicates whether a grid location exists or not
    gridLocExists = False

    #if the message piece is a special message
    if (len(lastDataPiece) == 3 and lastDataPiece == "RRR"):
        messageExists = True
        messageType = "special"
    elif (len(lastDataPiece) == 2 and lastDataPiece == "73"):
        messageExists = True
        messageType = "special"
    elif (len(lastDataPiece) == 4 and lastDataPiece == "RR73"):
        messageExists = True
        messageType = "special"
    #if the message piece is a recieved strength
    elif (len(lastDataPiece) == 3 and (lastDataPiece[0] == '-' or lastDataPiece[0] == '+') and lastDataPiece[1].isdigit and lastDataPiece[2].isdigit):
        messageExists = True
        messageType = "rec_str"
    #if the message piece looks like (ex: R-34)
    elif (len(lastDataPiece) == 4 and lastDataPiece[0] == 'R' and (lastDataPiece[1] == '-' or lastDataPiece[1] == '+') and lastDataPiece[2].isdigit() and lastDataPiece[3].isdigit()):
        messageExists = True
        messageType = "encoded"
    #if the message piece is the grid location
    elif (len(lastDataPiece) == 4 and lastDataPiece[0].isalpha() and lastDataPiece[1].isalpha() and lastDataPiece[2].isdigit() and lastDataPiece[3].isdigit()):
        messageExists = True
        messageType = "grid_loc"

    #go through each data piece in the current line being processed
    for i in range(len(dataList)):
        #get the current data piece of the line being processed
        dataPiece = dataList[i]

        #if the data piece is not apart of the payload
        if i < 7:
            #if there is an underscore in the current data
            #piece, the data needs to be further separated
            if i == 0 and dataPiece.find("_"):
                #split the data where the underscore is
                separatedData = dataPiece.split("_")
                
                #get the date and add it to the processed line list in a presentable format
                date = separatedData.pop(0)
                #converting date to UTC
                processedLineList.append("20" + date[0:2] + "-" + date[4:6] + "-" + date[2:4])
                #get the time and add it to the processed line list in a presentable format
                time = separatedData.pop(0)
                processedLineList.append(time[0:2] + ":" + time[2:4] + "." + time[4:6])
            
            #if there is no underscore, the data piece is processed normally
            else:
                processedLineList.append(dataPiece)

        #if the data piece is apart of the payload
        else:
            '''
            #if the current payload data piece is not the last piece of data (grid location)
            #if i != (len(dataList) - 1):
            if len(dataPiece) >= 2:
                #store the first two characters of the location prefix
                locationPrefix = dataPiece[0] + dataPiece[1]
            else:
                locationPrefix = dataPiece[0]

            if len(locationPrefix) >= 3 and locationPrefix[0] == '<':
                locationPrefix = dataPiece[1] + dataPiece[2]
            #find the index of the location in the dataframe
            #locationIndex = locDf.columns.get_loc()
            locationIndex = -1
            '''

            #if the message piece is a special message
            if (i == len(dataList) - 1) and messageType == "special": #len(dataPiece) == 3 and dataPiece == "RRR":
                processedLineList.append(dataPiece)
            #if the message piece is a recieved strength
            elif (i == len(dataList) - 1) and messageType == "rec_str": #len(dataPiece) == 3 and (dataPiece[0] == '-' or dataPiece[0] == '+') and dataPiece[1].isdigit and dataPiece[2].isdigit:
                processedLineList.append(dataPiece)
            #if the message piece looks like (ex: R-34)
            elif (i == len(dataList) - 1) and messageType == "encoded": #len(dataPiece) == 4 and dataPiece[0] == 'R' and (dataPiece[1] == '-' or dataPiece[1] == '+') and dataPiece[2].isdigit() and dataPiece[3].isdigit():
                processedLineList.append(dataPiece)
            #if the message piece is the grid location
            elif (i == len(dataList) - 1) and messageType == "grid_loc": #len(dataPiece) == 4 and dataPiece[0].isalpha() and dataPiece[1].isalpha() and dataPiece[2].isdigit() and dataPiece[3].isdigit():
                #since the message is the grid location, the grid location exists on this line of data
                gridLocExists = True

                #solving for latitude-----------------------------------------------
                step1Result = (ord(dataPiece[1]) - 65) * 10
                step2Result = ord(dataPiece[3]) - 48
                latitude = step1Result + step2Result - 90
                #solving for longitude----------------------------------------------
                step1Result = (ord(dataPiece[0]) - 65) * 20
                step2Result = (ord(dataPiece[2]) - 48) * 2
                longitude = (step1Result + step2Result) - 180
                #output add the grid coordinates into the processed data
                processedLineList.append(str(latitude) + " " + str(longitude))

                date = processedLineList[0]
                time = processedLineList[1]

                #year, month, day, hour, minute, second = when
                when = [int(date[0:4]), int(date[5:7]), int(date[8:10]), int(time[0:2]), int(time[3:5]), int(time[6:8])]
                #latitude, longitude = location
                location = [latitude, longitude]

                #calculate the sun data given the date, time, and location
                sun_azimuth, sun_elevation = sunpos(when, location)

                #add the sun data to the processed line
                processedLineList.append(str(sun_azimuth))
                processedLineList.append(str(sun_elevation))

                '''
                date = processedLineList[0]
                time = processedLineList[1]

                #if there is a 0 in front of the month, get rid of it for the UTC time
                if date[8] == '0':
                    date.replace('0', '')

                #get the UTC time for getting the location of the sun
                datetime = date + " " + time[0:5]

                sunPos = astral.sun(date, latitude, longitude)
                print(sunPos)

                
                loc = EarthLocation(latitude, longitude)
                altazframe = AltAz(obstime = datetime, location = loc)
                sunaltaz = get_sun(datetime).transform_to(altazframe)

                print(sunaltaz)

                
                #get the az (direction of sun), alt (altitude of sun)
                az, alt = ast.sun_az_alt(datetime, longitude, latitude)
                #get the sun time (if the sun is up in the area and time or not, etc)
                sunTime = ast.sun_time(datetime, longitude, latitude, alt, az)

                processedLineList.append(az)
                processedLineList.append(alt)
                processedLineList.append(sunTime)

                
                #get the sun time by using the UTC time
                sun_time = Time(UTC_time)
                #get the Earth location from the coordinates
                loc = EarthLocation.of_address(latitude, longitude)
                altaz = AltAz(obstime = sun_time, location = loc)
                zen_ang = get_sun(sun_time).transform_to(altaz).zen

                processedLineList.append(sun_time)
                processedLineList.append(zen_ang)
                '''

            #if the message piece is a callsign
            else:
                
                #if the current callsign being accessed is the last callsign, store it into the callsign list and add this list to the processed line list
                if ((i == len(dataList) - 1) and messageExists == False) or ((i == len(dataList) - 2) and messageExists == True):
                    callsigns = callsigns + dataPiece
                    callsignCounter = callsignCounter + 1
                    processedLineList.append(callsigns)
                    processedLineList.append(str(callsignCounter) + "_callsigns")

                    #if the message does not exist, include nan
                    if messageExists == False:
                        processedLineList.append("nan")

                #if the current callsign is not the last callsign, store it into the callsign list
                else:
                    callsignCounter = callsignCounter + 1
                    callsigns = callsigns + dataPiece + " "

                '''
                #check through the location dataframe to see if the location prefix exists
                for i in range(len(locDf)):
                    #if the location prefix was found in the panda, 
                    # get the index of the row it was found on
                    if locDf.iloc[i]["series_prefix"] == locationPrefix:
                        locationIndex = i
                '''
            '''
            #check if the first character could be dedicated for a single country
            elif locationPrefix[0] == 'N' or locationPrefix[0] == 'W' or locationPrefix[0] == 'K':
                location = "United States of America"
                locationIndex = "Found"
            elif locationPrefix[0] == 'B':
                location = "China (People's Republic of)"
                locationIndex = "Found"
            elif locationPrefix[0] == 'R':
                location = "Russian Federation"
                locationIndex = "Found"
            elif locationPrefix[0] == 'M' or locationPrefix[0] == 'G' or locationPrefix[0] == '2':
                location = "United Kingdom of Great Britain and Northern Ireland"
                locationIndex = "Found"
            elif locationPrefix[0] == 'I':
                location = "Italy"
                locationIndex = "Found"
            elif locationPrefix[0] == 'F':
                location = "France"
                locationIndex = "Found"
            #if the callsign looks like <...>, then no location was found
            elif locationPrefix[0] == ".":
                pass
            
            #if the callsign is CQ, then it represents calling all stations
            elif len(dataPiece) == 2 and locationPrefix == "CQ":
                location = "Calling all Stations"
                locationIndex = 0
            else:
                #check through the location dataframe to see if the location prefix exists
                for i in range(len(locDf)):
                    #if the location prefix was found in the panda, 
                    # get the index of the row it was found on
                    if locDf.iloc[i]["series_prefix"] == locationPrefix:
                        locationIndex = i
            

            #if we are not yet using the message piece of the data, it has to be a callsign
            if message == False:
                #if the location was found in the panda
                if locationIndex != -1:
                    if locationIndex != "Found":
                        #get the actual location from the index of the row where it was found
                        location = locDf.iloc[locationIndex, 2]
                    #add the location next to it's corresponding code
                    processedLineList.append(location) 
                #otherwise, no location was found in the panda
                else:
                    processedLineList.append("NO LOCATION FOUND")
            
            if the current payload data piece is a message
            else:
                if len(dataPiece) == 4 and dataPiece[0].isalpha() and dataPiece[1].isalpha() and dataPiece[2].isdigit() and dataPiece[3].isdigit():
                    #solving for latitude-----------------------------------------------
                    step1Result = (ord(dataPiece[1]) - 65) * 10
                    step2Result = ord(dataPiece[3]) - 48
                    latitude = step1Result + step2Result - 90

                    #solving for longitude----------------------------------------------
                    step1Result = (ord(dataPiece[0]) - 65) * 20
                    step2Result = (ord(dataPiece[2]) - 48) * 2
                    longitude = (step1Result + step2Result) - 180

                    processedLineList.append("(" + str(latitude) + ", " + str(longitude) + ")")
                #gridLocation = dataPiece
                #processedLineList.append(dataPiece)
                else:
                    processedLineList.append(dataPiece)
            '''
    #if the grid location was not included in this line of data, there was no sun data
    if gridLocExists == False:
        processedLineList.append("nan")
        processedLineList.append("nan")

    processedLineList.pop(3) #getting rid of Rx/Tx
    processedLineList.pop(3) #getting rid of FT4/FT8
    processedLineList.pop(5) #getting rid of freq offset

    #use to omit the payload
    #while(len(processedLineList) > 6):
        #processedLineList.pop(6)

    print(processedLineList)

    #return the processed line list after it is cleaned up
    return processedLineList

###########################################################
# function that will print the passed data into           #
# an output file that will be a csv file                  #
#                                                         #
# listToPrint is the data to be printed in the csv file.  #
###########################################################
def printToFile(listToPrint):
    #show user that the data will be printed to a csv file
    print("\n... printing data to csv file ...\n")

    #open the csv file that will store the cleaned data
    file = open("ham_data_reduced.csv", "w")

    #go through each line of data to separate
    #each data piece in each line with a comma
    for line in listToPrint:
        #go through each data piece in the current line
        for i in range(len(line)):
            #only separate data peices with a comma 
            #if the current data peice is not the last one
            if i != ( len(line) - 1 ):
                '''
                #if the current piece of data is not a list, output it normally
                if(type(line[i]) != list):
                '''
                print(line[i] + ",", end = " ")
                file.write(line[i] + ", ") 
                '''
                #otherwise, the current piece of data is a list, so print the contents in list format
                else:
                    listOfData = line[i]

                    #print("[", end = "")
                    #file.write("[")

                    for j in range(len(listOfData) - 1):
                        print(listOfData[j], end = " ")
                        file.write(listOfData[j] + " ") 

                    print(listOfData[len(listOfData) - 1] + ",", end = " ")
                    file.write(listOfData[len(listOfData) - 1] + ", ") 
                '''

            #otherwise, the last data peice will
            #be processed with no comma after
            else:
                print(line[i])
                file.write(line[i] + "\n")


    #close the csv file since the cleaned data has been stored
    file.close()

###########################################################
# main function that will be executed in runtime.         #
###########################################################
def main():
    #createPanda()
    
    #instantiate a new instance of the Path class and
    #initialize it with the file path that you want to check for existence
    path_to_file = 'ham_data_reduced.txt'
    path = Path(path_to_file)

    #try to open the data file
    print("\nwelcome to ham file")
    hamfile = open("ham_data_reduced.txt", "r")

    #check if the file exists using the is_file() method
    if path.is_file():
        print(f'The file {path_to_file} exists')
        #ask if you want to look at the data txt file you type yes or no
        print("this is a real file do you want to open it (yes/no):")
        why=input("\t>> ")

        #declare the list that will hold all processed lines 
        processedLinesMatrix = []

        #if the user wants to open the file
        if why == "yes":
            #show the user that the data will now be processed
            print("\n... processing data ...\n")
            #it will print the data sets
            lines = hamfile.readlines()

            #start timer to time how long it takes to process the data
            tic = time.perf_counter()
            #process each line of the data
            for line in lines:
                #process the current line of data by passing to the process func
                processedLine = process(line)
                #store previously processed line (list of data pieces) 
                #into the processed lines matrix
                processedLinesMatrix.append(processedLine)
            #end the timer to get how long it took to process the data
            toc = time.perf_counter()
            #show how long it took to process the data
            print(f"The data took {toc - tic:0.4f} seconds to process")

            #ask the user if they want to save the processed data into a csv file
            print("Do you want to save the processed data in a csv file? (yes/no): ")
            ans = input("\t>> ")

            #if the user answered yes, then print the data to the file
            if ans == "yes":
                #after the data has been stored in a matrix, pass that
                #matrix of processed values to be printed in a csv file
                printToFile(processedLinesMatrix)
            
        #ask the user if they want to see graphical representations of the data
        print("\nDo you want to see graphs of the data? (yes/no): ")
        ans = input("\t>> ")
        
        #if the user wants to see graphical representations of the
        #data, ask them which data pieces they want to see in a graph
        while ans == "yes":
            print("\n-------------------------------------")
            print("1: time (x-axis), freq offset (y-axis)")
            print("2: recieve strength (x-axis), freq offset (y-axis)")
            print("3: time offset (x-axis), freq offset (y-axis)")
            print("4: time (x-axis), recieve strength (y-axis)")
            print("5: time (x-axis), time offset (y-axis)")
            print("6: recieve strength (x-axis), time offset (y-axis)")
            print("Enter which info you want to plot: ")
            plotUserWantsToSee = input("\t>> ")

            #create the panda to store the info
            df = pd.read_csv("no_payload_ham_data.csv")
            df.columns = [ "date",
                "timestamp",
                "freq",
                "recieve_strength",
                "time_offset",
                "freq_offset" ]

            #if the user wants to see the time and freq offset graph
            if plotUserWantsToSee == "1":
                df.plot(kind = "scatter", x = "timestamp", y = "freq_offset")
                plt.xlim(140000, 240000)
            #if the user wants to see the recieve strength and freq offset graph
            elif plotUserWantsToSee == "2":
                df.plot(kind = "scatter", x = "recieve_strength", y = "freq_offset")
            #if the user wants to see the time offset and freq offset graph
            elif plotUserWantsToSee == "3":
                df.plot(kind = "scatter", x = "recieve_strength", y = "freq_offset")
            #if the user wants to see the time offset and freq offset graph
            elif plotUserWantsToSee == "4":
                df.plot(kind = "scatter", x = "time_offset", y = "freq_offset")
            #if the user wants to see the time and time offset graph
            elif plotUserWantsToSee == "5":
                df.plot(kind = "scatter", x = "timestamp", y = "time_offset")
                plt.xlim(140000, 240000)
            #if the user wants to see the recieve strength and time offset graph
            elif plotUserWantsToSee == "6":
                df.plot(kind = "scatter", x = "recieve_strength", y = "time_offset")

            #show the graph with the plotted points
            plt.show()

            #ask user if they want to keep seeing data graphs
            print("\nDo you want to see more figures of the data? (yes/no): ")
            ans = input("\t>> ")

        
        #if say no then you are done then it will go to
        #the end where you close the hamfile.    
        #else:
        print("you are done bye")
    else:
        print(f'The file {path_to_file} does not exist')

    hamfile.close()
    
if __name__=="__main__":
    main()  
