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
# function that will create a panda from a csv file       #
###########################################################
def createPanda():

    df = pd.read_csv("no_payload_ham_data.csv")
    df.columns = [ "date",
                    "timestamp",
                    "freq",
                    "recieve_strength",
                    "time_offset",
                    "freq_offset", ]
                    #"payload" ]
    print(df.to_string())

    #pd.pandas_data.info()
    #pd.pandas_data.describe()

###########################################################
# function that will process a line by                    #
# separating its components with commas                   #
#                                                         #
# li is the current line of data that is being processed. #
###########################################################
def process(li):
    #split the data and store its peices into a data list
    dataList = li.split()

    #the list that will hold the processed data
    processedLineList = []

    #go through each data piece in the current line being processed
    for i in range(len(dataList)):
        #get the current data piece of the line being processed
        dataPiece = dataList[i]

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
            #if (dataPiece != "Rx") and (dataPiece != "Tx") and (dataPiece != "FT8") and (dataPiece != "FT4"):
            #add the data piece to the processed line list
                processedLineList.append(dataPiece)

    #return the line after it is processed 
    #with commas between each piece of data
    #return the processed line list after it is cleaned up
    processedLineList.pop(3)
    processedLineList.pop(3)

    #use to omit the payload
    #while(len(processedLineList) > 6):
        #processedLineList.pop(6)

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
    file = open("hamDataV2.csv", "w")

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
    '''
    #instantiate a new instance of the Path class and
    #initialize it with the file path that you want to check for existence
    path_to_file = 'hamDataV2.TXT'
    path = Path(path_to_file)

    #try to open the data file
    print("\nwelcome to ham file")
    hamfile = open("hamDataV2.TXT", "r")

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
            '''
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
                print("Enter which info you want to plot: ")
                plotUserWantsToSee = input("\t>> ")

                #declare the lists that will hold graph coordinates
                #x_axis = []
                #y_axis = []

                #createPanda()
                df = pd.read_csv("no_payload_ham_data.csv")
                df.columns = [ "date",
                    "timestamp",
                    "freq",
                    "recieve_strength",
                    "time_offset",
                    "freq_offset" ]

                #make a new empty graph
                #plt.figure()
                #df.figure()

                #if the user wants to see the time and freq offset graph
                if plotUserWantsToSee == "1":
                    df.plot(kind = "scatter", x = "timestamp", y = "freq_offset")
                    '''
                    for i in range(70000):
                    #for i in range(1000):
                        #current line of data that will be used
                        #to extract the time and freq offset
                        line = processedLinesMatrix[i]
                        
                        #obtain the time and freq offset points
                        x_axis.append(int(line[1]))
                        y_axis.append(int(line[5]))
                    '''
                #if the user wants to see the recieve strength and freq offset graph
                elif plotUserWantsToSee == "2":
                    df.plot(kind = "scatter", x = "recieve_strength", y = "freq_offset")
                    '''
                    for i in range(70000):
                        #current line of data that will be used to
                        #extract the recieve strength and freq offset
                        line = processedLinesMatrix[i]
                        
                        #obtain the recieve strength and freq offset points
                        x_axis.append(int(line[3]))
                        y_axis.append(int(line[5]))
                        '''
                #if the user wants to see the time offset and freq offset graph
                elif plotUserWantsToSee == "3":
                    df.plot(kind = "scatter", x = "recieve_strength", y = "freq_offset")
                    '''
                    for i in range(70000):
                        #current line of data that will be used
                        #to extract the time offset and freq offset
                        line = processedLinesMatrix[i]
                        
                        #obtain the time offset and freq offset points
                        x_axis.append(float(line[4]))
                        y_axis.append(int(line[5]))
                    '''
                #if the user wants to see the time offset and freq offset graph
                elif plotUserWantsToSee == "4":
                    df.plot(kind = "scatter", x = "time_offset", y = "freq_offset")
                    '''
                    for i in range(70000):
                        #current line of data that will be used
                        #to extract the time offset and freq offset
                        line = processedLinesMatrix[i]
                        
                        #obtain the time offset and freq offset points
                        x_axis.append(float(line[1]))
                        y_axis.append(int(line[5]))
                    '''
                elif plotUserWantsToSee == "5":
                    df.plot(kind = "scatter", x = "timestamp", y = "time_offset")
                    '''
                    for i in range(70000):

                        line = processedLinesMatrix[i]

                        #time and time offset
                        x_axis.append(int(line[1]))
                        y_axis.append(float(line[4]))
                    '''
                elif plotUserWantsToSee == "6":
                    df.plot(kind = "scatter", x = "recieve_strength", y = ["time_offset", ])


                #plot with the corresponding points
                #plt.plot(x_axis, y_axis)
                #show the graph with the plotted points
                plt.show()

                #ask user if they want to keep seeing data graphs
                print("\nDo you want to see more figures of the data? (yes/no): ")
                ans = input("\t>> ")

        '''
        #if say no then you are done then it will go to
        #the end where you close the hamfile.    
        else:
              print("you are done bye")
    else:
        print(f'The file {path_to_file} does not exist')

    hamfile.close()

'''

if __name__=="__main__":
    main()  
