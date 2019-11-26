import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from zipfile import ZipFile
import datetime


zip_file = "../data/csv_comp_small.zip"

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
        
        #get mean and standard deviation
        #row[0].delete
        for row in file_data :
            try:
                if row[7] == 0 :
                    row.delete
            except :
                continue
        E_hp_mean = np.mean(file_data.E_hp)
        print(E_hp_mean)
        
        #print(file_data)
        i += 1
        if i >> 0:
            break



print("done")