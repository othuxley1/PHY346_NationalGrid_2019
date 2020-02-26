#import modules 
import csv 
import numpy as np 
import pandas as pd 
 
#This path should be set to the file location of the metadata on the local machine 
localPath = "C:/Users/rossh/Documents/PHY346/PHY346_NationalGrid_2019/data/7955_rhpp_metadata.csv" 
 
#Any HPIDs can be put here - these are currently just test values 
HPIDs = ("5504","5637","5332") 
 
def meta_reader(IDs,filePath): 
     
    #Creating an empty list that important data will be added to 
    collectedData = [] 
     
    #Using padnas methods to reduce the metadata down to only useful data 
    metadata = pd.read_csv(filePath) 
    metadata.set_index("Site.ID", inplace=True) 
    metaCols = [ "Heat.pump.type", "Site.type", "Property.Type", "Age.of.property", "Number.of.bedrooms", "Emitter.type", "Installer.net.capacity.corrected"] 
    metadata = metadata[metaCols] 
     
    #Reopening the file in a non pandas method 
    with open(filePath,newline='', encoding='utf-8') as csvFile: 
        csvReader = csv.reader(csvFile) 
    #Looping through every HPID inputted by the user 
    for ID in IDs: 
        i=-1 
        #Reopening the file 
        with open(filePath,newline='', encoding='utf-8') as csvFile: 
            csvReader = csv.reader(csvFile) 
            #Looping through every heat pump contained in the metadata 
            for row in csvReader: 
                #Checking the IP of the heat pump matches the searched ID 
                if (row[0])[4:8] == ID: 
                    #Short message to inform user that there was a match 
                    print("Heat Pump Found!") 
                    #Outputting the useful information for that heat pump 
                    collectedData.append((np.array(metadata))[i]) 
                    print(np.array(metadata)[i]) 
                i+=1                                 
    return(collectedData) 
 
meta_reader(HPIDs,localPath) 
