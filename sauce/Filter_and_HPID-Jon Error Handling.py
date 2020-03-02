# -*- coding: utf-8 -*-
"""
Created on Tue Feb 11 13:50:02 2020

@author: jonat
"""

from datetime import datetime
import numpy as np
import pandas as pd
import glob
import csv
from zipfile import ZipFile
import traceback

# Config
hp_folder = "C:/Users/prpge/Downloads/renewable_heat_premium_payment_CLEANED_small"
outfile = "C:/Users/prpge/Downloads/renewable_heat_premium_payment_CLEANED_small"
error_file = "Filter_and_HPID_error.txt"
# ==============


def all_HP_temp_filtered():  #csv of 15 min temp data for each HP
    
    cols = ["HPID", "H_hp", "E_hp", "temp"]
    data_df_15min = pd.DataFrame(columns=cols)

    for filename in glob.glob('{}/*.zip'.format(hp_folder)):
        with ZipFile(filename, 'r') as zip:
            zip.extractall()
    
    
    for filename in glob.glob('{}/*.csv'.format(hp_folder)):
        try:
            HPID = filename[-8:-4]
            print(HPID)                     #to show progress
            data_list_indi = []
            with open(filename, "r") as fid:
                next(fid)
                lines = fid.readlines() # list of strings for lines in the file            
                for line in lines:
                    row = line.strip("\n").split(",")
                    dt = datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S")
                    H_hp = np.nan if row[1] == "NA" else float(row[1])*0.03         #Wh every 2m ---> kW
                    E_hp = np.nan if row[7] == "NA" else float(row[7])*0.03
                    temp = np.nan if row[-3] == "NA" else float(row[-3])
                    data_list_indi.append([HPID, dt, H_hp, E_hp, temp,])
            cols = ["HPID","Datetime", "H_hp", "E_hp", "temp"]
            data_df_indi = pd.DataFrame(data_list_indi, columns=cols)
            data_df_indi = data_df_indi[data_df_indi.E_hp > 0.03]
            rows = len(data_df_indi.index)
            median = data_df_indi.loc[:,"E_hp"].median()
            iqr = data_df_indi.loc[:,"E_hp"].quantile(0.75) - data_df_indi.loc[:,"E_hp"].quantile(0.25)
            data_df_indi_filtered = data_df_indi[data_df_indi.E_hp < (median + 4*iqr)]
            rowsf = len(data_df_indi_filtered.index)
            ratio_filtered = (rows - rowsf) / rows
            print(ratio_filtered)
            data_df_indi_15min = data_df_indi_filtered.resample('15min',on='Datetime').max()
            data_df_indi_15min.drop("Datetime", axis=1, inplace=True)
            data_df_indi_15min.HPID.fillna(HPID, inplace=True)
            
            data_df_15min = data_df_15min.append(data_df_indi_15min)
            data_df_15min['Datetime'] = data_df_15min.index
        except Exception as err:
            print(err)
            with open(error_file, 'a') as fid:
                fid.write("\n" + HPID + "\n")
                fid.write(str(err))
                fid.write(traceback.format_exc())
                fid.write("\n ============================================================")
                
    data_df_15min.set_index("HPID", inplace=True)
    
    data_df_15min.to_csv ('{}/all_HP_table.csv'.format(outfile))
    print(data_df_15min)
    return data_df_15min

if __name__ == "__main__":
    all_HP_temp_filtered()