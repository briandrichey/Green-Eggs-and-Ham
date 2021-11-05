# regex library
import regex

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

    #go through each data piece in the current line being processed
    for i in range(len(dataList)):
        #get the current data piece of the line being processed
        dataPiece = dataList[i]

        #if the data piece is not apart of the payload
        if i < 7:
            #if there is an underscore in the current data
            #piece, the data needs to be further separated
            if dataPiece.find("_"):
                #split the data where the underscore is
                separatedData = dataPiece.split("_")
                    
                #store the separated data peices into the processed line
                for sepDataPiece in separatedData:
                    processedLineList.append(sepDataPiece)
            
            #if there is no underscore, the data piece is processed normally
            else:
                processedLineList.append(dataPiece)

        #if the data piece is apart of the payload
        else:
            #if the current payload data piece is not the last piece of data (grid location)
            if i != (len(dataList) - 1):
                #store the first two characters of the location prefix
                locationPrefix = dataPiece[0] + dataPiece[1]
                #find the index of the location in the dataframe
                #locationIndex = locDf.columns.get_loc()
                locationIndex = -1
                #check through the location dataframe to see if the location prefix exists
                for i in range(len(locDf)):
                    #if the location prefix was found in the panda, 
                    # get the index of the row it was found on
                    if locDf.iloc[i]["series_prefix"] == locationPrefix:
                        locationIndex = i

                #if the location was found in the panda
                if locationIndex != -1:
                    #get the actual location from the index of the row where it was found
                    location = locDf.iloc[locationIndex, 2]
                    #add the location next to it's corresponding code
                    processedLineList.append(location) 
                #otherwise, no location was found in the panda
                else:
                    processedLineList.append("NO LOCATION FOUND")
            #if the current payload data piece is the grid location
            else:
                gridLocation = dataPiece

    processedLineList.pop(3) #getting rid of Rx/Tx
    processedLineList.pop(3) #getting rid of FT4/FT8

    #use to omit the payload
    #while(len(processedLineList) > 6):
        #processedLineList.pop(6)

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
    file = open("ham_data.csv", "w")

    #go through each line of data to separate
    #each data piece in each line with a comma
    for line in listToPrint:
        #go through each data piece in the current line
        for i in range(len(line)):
            #only separate data peices with a comma 
            #if the current data peice is not the last one
            if i != ( len(line) - 1 ):
                print(line[i] + ",", end = " ")
                file.write(line[i] + ", ")
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

            #process each line of the data
            for line in lines:
                #process the current line of data by passing to the process func
                processedLine = process(line)
                #store previously processed line (list of data pieces) 
                #into the processed lines matrix
                processedLinesMatrix.append(processedLine)

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
