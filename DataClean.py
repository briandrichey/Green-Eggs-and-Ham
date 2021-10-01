# upload libraries to clean data with commas
from pathlib import Path
import os
import sys

###########################################################
# function that will process a line by                    #
# separating its components with commas                   #
#                                                         #
# li is the current line of data that is being processed. #
###########################################################
def process(li):
    #split the data and store its peices into a data list
    dataList = li.split()

    #string that will store a line of processed data 
    #with all pieces of data separated with commas 
    #(ex: 210422, 164445, 14.074, Rx, FT8, 5, 0.2, 1942, CQ, K8TE, DM65)
    processLine = ""

    for i in range(len(dataList)):
        #only separate data peices with a comma 
        #if the current data peice is not the last one
        if i != ( len(dataList) - 1 ):

            #if there is an underscore in the current data
            #piece, the data needs to be further separated
            if dataList[i].find("_"):
                #split the data where the underscore is
                separatedData = dataList[i].split("_")

                #store the separated data peices into the processed line
                for sepDataPiece in separatedData:
                    processLine += sepDataPiece + ", "
            #if there is no underscore, the data piece is processed normally
            else:
                processLine += dataList[i] + ", "

        #otherwise, the last data peice will
        #be processed with no comma after
        else:
            processLine += dataList[i]

    #return the line after it is processed 
    #with commas between each piece of data
    return processLine

###########################################################
# main function that will be executed in runtime.         #
###########################################################
def main():
    #instantiate a new instance of the Path class and
    #initialize it with the file path that you want to check for existence
    path_to_file = 'ham_data.txt'
    path = Path(path_to_file)

    print("welcome to ham file")
    hamfile = open("ham_data.txt", "r")

    #check if the file exists using the is_file() method
    if path.is_file():
        print(f'The file {path_to_file} exists')
        #ask if you want to look at the data txt file you type yes or no
        print("this is a real file do you want to open it (yes/no):")
        why=input()

        #if the user wants to open the file
        if why == "yes":
            #show the user that the data will now be processed
            print("\n... processing data ...\n")
            #it will print the data sets
            lines = hamfile.readlines()
            for line in lines:
                #process each line before sending it into csv file
                processedLine = process(line)
                print(processedLine)

        #if say no then you are done then it will go to
        #the end where you close the hamfile.    
        else:
              print("you are done bye")
    else:
        print(f'The file {path_to_file} does not exist')

    hamfile.close()
if __name__=="__main__":
    main()
