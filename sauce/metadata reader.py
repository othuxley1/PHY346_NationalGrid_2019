# -*- coding: utf-8 -*-
"""
Created on Wed Feb 19 13:45:27 2020

@author: prpge
"""
#importing modules
import csv
import numpy as np
import pandas as pd
import glob
from zipfile import ZipFile
import traceback
import sys

#config
#This path should be set to the location of the metadata
filePath = "C:/Users/prpge/Downloads/7955_rhpp_metadata.csv"
#This path should be set to location of the rhpp zip
zipPath = "C:/Users/prpge/Downloads/renewable_heat_premium_payment_CLEANED_small"
#Error file path
error_file = "metadata_reader_error.txt"
#Large metadata file
meta_file = "metadata_collected.txt"

#Any HPIDs can be put here - these are currently just test values
HPIDs = ("5504","5637","5332")

def meta_reader(metaPath,IDs=0,rhppPath=0):
    
    #Creating  empty lisst that will be used to write to file
    collectedData = []
    HPIDs = []
    #Using pandas methods to reduce the metadata down to only useful data
    metadata = pd.read_csv(metaPath)
    metadata.set_index("Site.ID", inplace=True)
    metaCols = [ "Heat.pump.type", "Site.type", "Property.Type", "Age.of.property", "Number.of.bedrooms", "Emitter.type", "Installer.net.capacity.corrected"]
    metadata = metadata[metaCols]
    
    #Reopening the file in a non pandas method
    with open(metaPath,newline='', encoding='utf-8') as csvFile:
        csvReader = csv.reader(csvFile)
    if rhppPath == 0 and IDs !=0:
    #Looping through every HPID inputted by the user
        for ID in IDs:
            i=-1
            #Reopening the file
            with open(metaPath,newline='', encoding='utf-8') as csvFile:
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
    elif rhppPath != 0:
        print("rhppPath loaded successfully")
        for filename in glob.glob('{}/*.zip'.format(rhppPath)):
            with ZipFile(filename, 'r') as Zip:
                Zip.extractall()
        for filename in glob.glob('{}/*.csv'.format(rhppPath)):
            HPID = filename[-8:-4]
            try:
                i = -1
                with open(metaPath,newline='', encoding='utf-8') as csvFile:
                    csvReader = csv.reader(csvFile)
                    for row in csvReader:
                        if (row[0])[4:8] == HPID:
                            print("Heat Pump Found!")
                            HPIDs.append(HPID)
                            collectedData.append((np.array(metadata))[i])
                            print(np.array(metadata)[i])
                        i += 1
            except Exception as err:
                print(err)
                with open(error_file, 'a') as fid:
                    fid.write("\n" + HPID + "\n")
                    fid.write(str(err))
                    fid.write(traceback.format_exc())
                    fid.write("\n ============================================================")
    else:
        print("Error: Provide either HPIDs or a file path")
        sys.exit()
    with open(meta_file, 'w') as fud:
        for data,name in zip(collectedData,HPIDs):
            fud.write(name + str(data) + "\n")
    return(collectedData)

if __name__ == "__main__":
    meta_reader(filePath,HPIDs,zipPath)
