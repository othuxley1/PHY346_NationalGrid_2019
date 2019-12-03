import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from zipfile import ZipFile
import datetime

zip_file = "../data/csv_comp_small.zip"
#zip_file = "C:/Users/prpge/Downloads/rhpp_small.zip"

with ZipFile(zip_file, "r") as myzip:
    file_paths = [file  for file in myzip.namelist() if ".csv" in file]



hp_ids = []
        
with ZipFile(zip_file, "r") as myzip:
    i = 0            
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
        
        
        #Delete any 0 values
        for row in file_data :
            try:
                if row[7] == 0 :
                    row.delete
            except :
                continue
        
        #choosing the useful critera from the csv
        useful_headers = ["E_hp","temperature","precipitation","wind_speed"]
        useful_data = file_data[useful_headers].copy()
        
        #wiping all NaN values from the data
        clean_data = useful_data.dropna()

        #Grouping the cleaned data by day
        group_daily = clean_data.groupby(pd.Grouper(freq='D'))
        #Checking how many values each day has...
        #And disregarding those with NaN values
        count_df = group_daily.count()
        valid_days = count_df == 720
        #Creating a sum of all important useful data
        daily_sum = group_daily.sum()
        #how to select data: ' daily_sum[valid_days] 
        #Getting a sum of all E_hp useage per day 
        E_hp_daily_sum = daily_sum[valid_days]["E_hp"]

        #Getting mean values of E_hp
        E_hp_mean = np.mean(file_data.E_hp)
        print(E_hp_mean)
        i += 1
        
#        if i >> 0:
#            break
print("done")