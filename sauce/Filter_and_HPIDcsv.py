#import modules 
import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt 
from zipfile import ZipFile 
import datetime 
from scipy import stats 
import glob
import csv
 
    #get data and metadata 
zip_file = "../data/csv_comp_small.zip" 
 
metafile = "../data/7955_rhpp_metadata.csv" 
metadata = pd.read_csv(metafile) 
metadata.set_index("Site.ID", inplace=True) 
    #get useful columns from metadata 
metadata 
meta_cols = [ "Heat.pump.type", "Site.type", "Property.Type", "Age.of.property", "Number.of.bedrooms", "Emitter.type", "Installer_net_capacity_corrected"] 
metadata[meta_cols] 

    #get file paths 
with ZipFile(zip_file, "r") as myzip: 
    file_paths = [file  for file in myzip.namelist() if ".csv" in file] 
    hp_ids = [] 

    #set up figure 
#figure_main = plt.figure(figsize = (12,5)) 
#define variables
cols_15min = ["hp_id", "H_hp", "E_hp", "temp"]
data_df_15min = pd.DataFrame(columns=cols_15min)
data_list_indi = []

 
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
        lines = file_data.readlines() # list of strings for lines in the file 
        print(lines)
        for line in lines: 
                row = line.strip("\n").split(",") 
                dt = datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S")
                print(dt)
                #sets NA values to NaNs
                H_hp = np.nan if row[1] == "NA" else float(row[1])*0.03
                E_hp = np.nan if row[7] == "NA" else float(row[7])*0.03    #converts Wh/2min to KW
                temp = np.nan if row[-3] == "NA" else float(row[-3]) 
                data_list_indi.append([hp_id, dt, H_hp, E_hp, temp,]) 
        
        
        
        print(data_list_indi)
        cols = ["hp_id","Datetime", "H_hp", "E_hp", "temp"] 
        data_df_indi = pd.DataFrame(data_list_indi, columns=cols) 
        data_df_indi = data_df_indi[data_df_indi.E_hp > 0.03]    
        
        #get statistical data
        #median = np.median(data_df_indi.E_hp)
        median = 5
        iqr = stats.iqr(data_df_indi.E_hp)
        print(median, iqr)
        #filter out outlying values
        data_df_indi_filtered = data_df_indi[data_df_indi.E_hp < (median + 4*iqr)] 
        data_df_indi_15min = data_df_indi_filtered.resample('15min',on='Datetime').max() 
        data_df_indi_15min.drop("Datetime", axis=1, inplace=True) 
        data_df_indi_15min.hp_id.fillna(hp_id, inplace=True) 
        
        data_df_15min = data_df_15min.append(data_df_indi_15min) 
        data_df_15min['Datetime'] = data_df_15min.index 
        
        
        
        
        
        # create DatetimeIndex
        #file_data.Record_time = pd.to_datetime(file_data.Record_time)
        #file_data.set_index("Record_time", inplace=True) 
        #file_data.E_hp = file_data.E_hp*0.03 #convert E_Hp from Wh/2min to KW equiv.
        #Old outliers (statistical method) 
        #get mean and standard deviation 
        #indices = file_data.E_hp > 0.03 
        #greater_than_one = (file_data.loc[indices, "E_hp"]) 
        #median = np.median(greater_than_one) 
        #iqr = stats.iqr(greater_than_one) 
         
         
        #get outliers 
         
        #outliers = greater_than_one[ greater_than_one > (median + 4*iqr)] 
        #file_data.loc[outliers.index, :] = np.nan 
        #outlier_number = len(outliers) 
        #print(outlier_number) 
        #use metadata to get more outliers 
        ''' 
        #Logical outliers (power usage > hp maximum power) 
        hp_capacity = metadata.Installer_net_capacity_corrected[]
         
        print(hp_capacity) 
        outliers = file_data.loc(file_data.E_hp * 0.03 > hp_capacity) 
        file_data.loc[outliers.index, :] = np.nan 
        '''
        '''
        #plot data 
        file_data.E_hp.plot() 
        axes = plt.gca() 
        axes.set_ylim([0,30]) 
        plt.ylabel("E_hp [KW]") 
        figure_main.add_subplot() 
        '''

        i += 1 
        if i > 1: 
            break 

#data_df_15min.set_index("HPID", inplace=True)
    
#data_df_15min.to_csv ("../data/all_HP_table.csv")
#print(data_df_15min)         
 
#figure_main.show() 
#plt.savefig('all_data.png', bbox_inches='tight') 
print("done")



