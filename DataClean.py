# upload libraries to clean data with commas
from pathlib import Path
import os
import sys
def main():
    
    # instantiate a new instance of the Path class and
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
        
        if why == "yes":
            #it will print the data sets
            lines = hamfile.readlines()
            for line in lines:
                print(line)
                
        #if say no then you are done then it will go to
        #the end where you close the hamfile.    
        else:
              print("you are done bye")
    else:
        print(f'The file {path_to_file} does not exist')

    hamfile.close()
if __name__=="__main__":
    main()  
