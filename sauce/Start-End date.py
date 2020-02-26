#import modules
from datetime import datetime 
import numpy as np 
import pandas as pd 
import glob 
import csv 
import os
import traceback

# Config 
hp_folder = "C:/Users/rossh/Documents/PHY346/PHY346_NationalGrid_2019/data/csv_small" #file path of hp csv's
outfile = "C:/Users/rossh/Documents/PHY346/PHY346_NationalGrid_2019/sauce"  #file path for saving data
error_file = "start_end_date_error.txt"
# ============== 
 
def indi_HP_table():    #csv of every HP's start & end times and data for amount of E_hp & H_hp NA values 
    data_list = [] 

    for filename in glob.glob('{}/*.csv'.format(hp_folder)): 
        try:       
            data_list_single = [] 
            print(filename)                  # to show progress 
            with open(filename, "r") as fid: 
                next(fid) 
                lines = fid.readlines() # list of strings for lines in the file             
                for line in lines: 
                    row = line.strip("\n").split(",") 
                    dt = datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S") 
                    H_hp = np.nan if row[1] == "NA" else float(row[1]) 
                    E_hp = np.nan if row[7] == "NA" else float(row[7]) 
                    temp = np.nan if row[-3] == "NA" else float(row[-3]) 
                    wind = np.nan if row[-1] == "NA" else float(row[-1]) 
                    precip = np.nan if row[-2] == "NA" else float(row[-2]) 
                    data_list_single.append([dt, H_hp, E_hp, temp, wind, precip]) 
            cols = ["Datetime", "H_hp", "E_hp", "temp", "wind", "precip"] 
            data_df = pd.DataFrame(data_list_single, columns=cols) 
            data_df.set_index("Datetime", inplace=True) 
         
            HPID = filename[-8:-4]
            print("HPID = ", HPID)
            start = data_df.index[0] 
            end = data_df.index[-1] 
            no_NA_Hhp = data_df.H_hp.isna().sum() 
            fraction_NA_Hhp = no_NA_Hhp / (data_df.H_hp.count() + no_NA_Hhp) 
            no_NA_Ehp = data_df.E_hp.isna().sum() 
            fraction_NA_Ehp = no_NA_Ehp / (data_df.E_hp.count() + no_NA_Ehp) 
            data_list.append([HPID, start, end, no_NA_Hhp, fraction_NA_Hhp, no_NA_Ehp, fraction_NA_Ehp]) 
        #check for errors and save errors found to a file
        except Exception as err:
            print(err)
#            if not os.path.isfile(error_file):
#                with open(error_file, 'w') as fid:
#                    fid.write("\n" + filename[4:8] + "\n")
#                    fid.write(str(err))
#                    fid.write(traceback.format_exc())
#                    fid.write("\n ============================================================")
            with open(error_file, 'a') as fid:
                fid.write("\n" + filename[4:8] + "\n")
                fid.write(str(err))
                fid.write(traceback.format_exc())
                fid.write("\n ============================================================")

    cols = ["HPID", "Start", "End", "#NA H_hp", "fraction NA H_hp", "#NA E_hp", "fraction NA E_hp"] 
    NA_data_df = pd.DataFrame(data_list,columns=cols) 
    NA_data_df.set_index("HPID", inplace=True) 
     
    NA_data_df.to_csv (r'{}/individual_HP_table.csv'.format(outfile)) 
    print(NA_data_df) 
    return(NA_data_df)
    
    
if __name__ == "__main__":
    indi_HP_table()