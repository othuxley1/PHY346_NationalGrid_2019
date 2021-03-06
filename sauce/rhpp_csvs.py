import pandas as pd
import numpy as np
import os
import glob
import h5py
from IPython.core.debugger import set_trace
import sys
import matplotlib.pyplot as plt
#from generic_tools import print_progress
from zipfile import ZipFile
import multiprocessing
import datetime

def main():
    
    zip_file = "../data/csv_comp_small.zip"

    
    with ZipFile(zip_file, "r") as myzip:
        file_paths = [file  for file in myzip.namelist() if ".csv" in file]



    print(file_paths)

    #get metadata file. 7955 for cleaned data
    metafile = "../data/7955_rhpp_metadata.csv"
    metadata = pd.read_csv(metafile)
    metadata.set_index("Site.ID", inplace=True)
    #print(metadata)
    
    #get useful columns from metadata
    metadata
    meta_cols = [
    "Heat.pump.type",
    "Site.type",
    "Property.Type",
    "Age.of.property",
    "Number.of.bedrooms",
    "Emitter.type",
    "Installer.net.capacity.as.recorded"]

    metadata[meta_cols]
    #print(metadata[meta_cols])
    def mung_rhpp_files(file_paths):
        """
        Open all rhpp files and save to hdf5 filestore.
        """
    
        i = 0
        N = len(file_paths)
        #print_progress(0, N)
        hp_ids = []
        
        with ZipFile(zip_file, "r") as myzip:
            
    
            for file in file_paths:
    
                # extract heatpump id
                hp_id = file[-12:-4].upper()
                hp_ids.append(hp_id)
    
                # load heatpump data from file
                
                
                file_object = myzip.open(file)
                file_data = pd.read_csv(file_object)
    
                # create DatetimeIndex
                file_data.Record_time = pd.to_datetime(file_data.Record_time)
                file_data.set_index("Record_time", inplace=True)
                
                # think carefully - you don't want to sum the temperature etc
                day_sum = file_data.groupby(pd.Grouper(freq='D')).sum()
                hour_sum = file_data.groupby(pd.Grouper(freq='H')).sum()
                #import pdb; pdb.set_trace()
                #print(hour_sum.E_hp)
                print(file)

                # for aggregation of all hps
                # ToDo
                # aggregate per half hour
                # store rolling half hour sum in python script
                # save to file
                
                # for daily aggregation
                # TODO
                # calculate aggregated values
                # store in python script
                # save to file 
    
                i += 1
                #usage_daily = plt.figure(figsize=(15,5))
                #plt.plot(day_sum.E_hp*0.03)
                #plt.title=(file)
                
                print("loop done")
                if i>>0:
                    break
                #print_progress(i, N)
            fig = plt.figure()
            usage_hourly = plt.figure(figsize=(15,5))
            plt.plot(day_sum.E_hp*0.03)
            plt.title=("hourly")
            axes = plt.gca()
            axes.set_ylim([0,2000])
            #axes.set_xlim([datetime.date(2014, 1, 1), datetime.date(2014, 2, 1)])
            
            
            usage_daily = plt.figure(figsize=(15,5))
            plt.plot(day_sum.E_hp*0.03)
            plt.title=("daily")
            
    mung_rhpp_files(file_paths)

main()


print("done")