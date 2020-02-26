import numpy as np
import pandas as pd
from zipfile import ZipFile
import datetime
import csv

file_path = "../data/csv_comp_small.zip"
#file_path = "C:/Users/prpge/Downloads/rhpp_small.zip"

def rhpp_data_profile(zip_file):
    with ZipFile(zip_file, "r") as myzip:
        file_paths = [file  for file in myzip.namelist() if ".csv" in file]



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
            daily_mean = group_daily.mean()
            daily_median= group_daily.median()
            daily_max = group_daily.max()
            daily_min = group_daily.min()
            daily_range = daily_max - daily_min   #(NEED TO ASK OWEN ABOUT THIS)
            
            #how to select data: ' daily_sum[valid_days] 
            #Getting a sum of all E_hp useage per day 
            E_hp_daily_sum = daily_sum[valid_days]["E_hp"]
            
            #Getting a range of data related to daily temperature
            temp_daily_mean = daily_mean[valid_days]["temperature"]
            temp_daily_median= daily_median[valid_days]["temperature"]
            temp_daily_max=daily_max[valid_days]["temperature"]
            temp_daily_min=daily_min[valid_days]["temperature"]
            temp_daily_range=daily_range[valid_days]["temperature"]
            
            #Getting a range of data related to wind speed
            wind_speed_daily_mean=daily_mean[valid_days]["wind_speed"]
            wind_speed_daily_median=daily_median[valid_days]["wind_speed"]
            wind_speed_daily_max=daily_max[valid_days]["wind_speed"]
            wind_speed_daily_min=daily_min[valid_days]["wind_speed"]
            wind_speed_daily_range=daily_range[valid_days]["wind_speed"]
            
            #Getting a range of data related to precipitiation
            precip_daily_mean=daily_mean[valid_days]["precipitation"]
            precip_daily_median=daily_median[valid_days]["precipitation"]
            precip_daily_max=daily_max[valid_days]["precipitation"]
            precip_daily_min=daily_min[valid_days]["precipitation"]
            precip_daily_range=daily_range[valid_days]["precipitation"]

            #Writing the csv file with the data collected 
            data_collection = np.vstack((E_hp_daily_sum,temp_daily_mean,temp_daily_median,temp_daily_max,temp_daily_min, temp_daily_range, wind_speed_daily_mean, wind_speed_daily_median, wind_speed_daily_max, wind_speed_daily_min, wind_speed_daily_range, precip_daily_mean, precip_daily_median, precip_daily_max, precip_daily_min, precip_daily_range))
            with open('Testing_file.csv', mode='w') as data_profile:
                row_writer = csv.writer(data_profile,delimiter=',',quotechar='"',quoting=csv.QUOTE_MINIMAL)
                row_writer.writerow(["E_hp","Temp Mean","Temp Median","Temp Max","Temp Min","Temp Range","Wind Speed Mean","Wind Speed Median","Wind Speed Max","Wind Speed Min","Wind Speed Range","Precip Mean","Precip Median","Precip Max","Precip Min","Precip Range"])
                for item in np.transpose(data_collection):
                    row_writer.writerow(item)
                continue
    print("Done!")
    return

def rhpp_data_filter(zip_file):
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
    return

rhpp_data_filter(file_path)
'''
choice = input("Run daily sum funciton Y/N?")
while choice is str:
    if choice == "Y":
        rhpp_data_profile(file_path)
    elif choice == "N":
        break
choice = input("Run filter function Y/N?")
while choice is str:
    if choice == "Y":
        rhpp_data_filter(file_path)
    elif choice == "N":
        break
'''