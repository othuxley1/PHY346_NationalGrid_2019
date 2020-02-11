# -*- coding: utf-8 -*-
"""
Created on Tue Feb 11 11:44:43 2020

@author: jonat
"""

#import modules 
import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt 
from zipfile import ZipFile 
import datetime 
from scipy import stats 
from datetime import datetime
import glob
import csv
 
 
#get data and metadata 
zip_file = "../data/csv_comp_small.zip" 
 
metafile = "../data/7955_rhpp_metadata.csv" 
metadata = pd.read_csv(metafile) 
metadata.set_index("Site.ID", inplace=True) 
    #get useful columns from metadata 
metadata 
meta_cols = [ 
"Heat.pump.type", 
"Site.type", 
"Property.Type", 
"Age.of.property", 
"Number.of.bedrooms", 
"Emitter.type", 
"Installer_net_capacity_corrected"] 
 
metadata[meta_cols] 
 
#get file paths 
with ZipFile(zip_file, "r") as myzip: 
    file_paths = [file  for file in myzip.namelist() if ".csv" in file] 
 
hp_ids = [] 
 
figure_main = plt.figure(figsize = (12,5)) 
      
with ZipFile(zip_file, "r") as myzip: 
    i = 0             
    for file in file_paths: 
        print(file) 
         
        # extract heatpump id 
        hp_id = file[-12:-4].upper() 
        hp_ids.append(hp_id) 
         
        # load heatpump data from file 
        file_object = myzip.open(file) 
        file_data = pd.read_csv(file_object) 
        # create DatetimeIndex 
        file_data.Record_time = pd.to_datetime(file_data.Record_time) 
        file_data.set_index("Record_time", inplace=True) 
        file_data.E_hp = file_data.E_hp*0.03 #convert E_Hp from Wh/2min to KW equiv. 
         
        #Old outliers (statistical method) 
        #get mean and standard deviation 
        indices = file_data.E_hp > 0.03 
        greater_than_one = (file_data.loc[indices, "E_hp"]) 
        median = np.median(greater_than_one) 
        iqr = stats.iqr(greater_than_one) 
        print(median, iqr) 
         
        #get outliers 
         
        outliers = greater_than_one[ greater_than_one > (median + 4*iqr)] 
        file_data.loc[outliers.index, :] = np.nan 
        outlier_number = len(outliers) 
        print(outlier_number) 
         
        ''' 
        #Logical outliers (power usage > hp maximum power) 
        hp_capacity = metadata[10] 
         
        print(hp_capacity) 
        outliers = file_data.loc(file_data.E_hp * 0.03 > hp_capacity) 
        file_data.loc[outliers.index, :] = np.nan 
        ''' 
        #plot data 
        file_data.E_hp.plot() 
        axes = plt.gca() 
        axes.set_ylim([0,30]) 
        plt.ylabel("E_hp [KW]") 
        figure_main.add_subplot() 
         
        #save file 
         
        #np.savetxt('5103_test_save', np.array(file_data[0]), header = 'true', delimiter=',') 
        #file_data.to_csv(',') 
         
         
        #import pdb; pdb.set_trace() 
        i += 1 
        if i > 5: 
            break 
         
 
figure_main.show() 
plt.savefig('all_data.png', bbox_inches='tight') 
print("done")




def all_HP_temp():  #csv of 15 min temp data for each HP
    
    cols = ["HPID", "H_hp", "E_hp", "temp"]
    data_df_15min = pd.DataFrame(columns=cols)
    
    for filename in glob.glob('*.csv'):
        HPID = filename[4:8]
        print(HPID)                     #to show progress
        data_list_indi = []
        with open(filename, "r") as fid:
            next(fid)
            lines = fid.readlines() # list of strings for lines in the file            
            for line in lines:
                row = line.strip("\n").split(",")
                dt = datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S")
                H_hp = np.nan if row[1] == "NA" else float(row[1])
                E_hp = np.nan if row[7] == "NA" else float(row[7])
                temp = np.nan if row[-3] == "NA" else float(row[-3])
                data_list_indi.append([HPID, dt, H_hp, E_hp, temp,])
        cols = ["HPID","Datetime", "H_hp", "E_hp", "temp"]
        data_df_indi = pd.DataFrame(data_list_indi, columns=cols)
        data_df_indi_15min = data_df_indi.resample('15min',on='Datetime').max()
        data_df_indi_15min.drop("Datetime", axis=1, inplace=True)
        data_df_indi_15min.HPID.fillna(HPID, inplace=True)
        
        data_df_15min = data_df_15min.append(data_df_indi_15min)
        data_df_15min['Datetime'] = data_df_15min.index
                
    data_df_15min.set_index("HPID", inplace=True)
    
    data_df_15min.to_csv (r'C:\Users\jonat\GitKraken_Code\PHY346_NationalGrid_2019\sauce\all_HP_table.csv')
    print(data_df_15min)
    return data_df_15min