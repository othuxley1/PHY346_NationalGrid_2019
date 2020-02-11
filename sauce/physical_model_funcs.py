# -*- coding: utf-8 -*-
"""
Created on Mon Nov 25 14:21:39 2019

@author: jonat
"""
from datetime import datetime
import numpy as np
import pandas as pd
import glob
import csv

def load_rhpp_csvs(file_path):
    data_list = []
    with open(file_path, "r") as fid:
        next(fid)
        lines = fid.readlines() # list of strings for lines in the file            
        for line in lines:
            row = line.strip("\n").split(",")
            dt = datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S")
            H_hp = np.nan if row[1] == "NA" else float(row[1])
            temp = np.nan if row[-3] == "NA" else float(row[-3])
            wind = np.nan if row[-1] == "NA" else float(row[-1])
            precip = np.nan if row[-2] == "NA" else float(row[-2])
            data_list.append([dt, H_hp, temp, wind, precip])
    cols = ["Datetime", "H_hp", "temp", "wind", "precip"]
    data_df = pd.DataFrame(data_list, columns=cols)
    data_df.set_index("Datetime", inplace=True)
    return data_df
    
def main():
    file_path = "rhpp5103.csv"
    load_rhpp_csvs(file_path)

def indi_HP_table():    #csv of every HP's start & end times and data for amount of E_hp & H_hp NA values
    data_list = []
    
    for filename in glob.glob('*.csv'):
        
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
    
        HPID = filename[4:8]
        start = data_df.index[0]
        end = data_df.index[-1]
        no_NA_Hhp = data_df.H_hp.isna().sum()
        fraction_NA_Hhp = no_NA_Hhp / (data_df.H_hp.count() + no_NA_Hhp)
        no_NA_Ehp = data_df.E_hp.isna().sum()
        fraction_NA_Ehp = no_NA_Ehp / (data_df.E_hp.count() + no_NA_Ehp)
        data_list.append([HPID, start, end, no_NA_Hhp, fraction_NA_Hhp, no_NA_Ehp, fraction_NA_Ehp])
    
    cols = ["HPID", "Start", "End", "#NA H_hp", "fraction NA H_hp", "#NA E_hp", "fraction NA E_hp"]
    NA_data_df = pd.DataFrame(data_list,columns=cols)
    NA_data_df.set_index("HPID", inplace=True)
    
    NA_data_df.to_csv (r'C:\Users\jonat\GitKraken_Code\PHY346_NationalGrid_2019\sauce\individual_HP_table.csv')
    print(NA_data_df)
    return(NA_data_df)

def number_readings():  #csv each for E_hp and H_hp - no. readings normalised to total possible for all HPs
    H_hp_count_dict = {}
    E_hp_count_dict = {}
    count = 0
    
    for filename in glob.glob('*.csv'):
        count += 1
        print(filename)                  # to show progress
        with open(filename, "r") as fid:
            next(fid)
            lines = fid.readlines() # list of strings for lines in the file
            
            for line in lines:
                row = line.strip("\n").split(",")
                dt = datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S")
                H_hp = np.nan if row[1] == "NA" else float(row[1])
                E_hp = np.nan if row[7] == "NA" else float(row[7])
                date_str = dt.date().strftime("%Y-%m-%d")
                
                if date_str in H_hp_count_dict:
                    if  not np.isnan(H_hp):
                        H_hp_count_dict[date_str] += 1
                else:
                    if not np.isnan(H_hp):
                        H_hp_count_dict[date_str] = 1
                        
                if date_str in E_hp_count_dict:
                    if  not np.isnan(E_hp):
                        E_hp_count_dict[date_str] += 1
                else:
                    if not np.isnan(E_hp):
                        E_hp_count_dict[date_str] = 1
                
    for i in H_hp_count_dict:               #normalisation
        H_hp_count_dict[i] = float(H_hp_count_dict[i]/(count*720))
    for i in E_hp_count_dict:
        E_hp_count_dict[i] = float(E_hp_count_dict[i]/(count*720))
    
    H_hp_list = []
    cols = ["Datetime", "Normalised number H_hp readings"]
    H_hp_df = pd.DataFrame(H_hp_list, columns = cols)
    H_hp_df.to_csv (r'C:\Users\jonat\GitKraken_Code\PHY346_NationalGrid_2019\sauce\number_readings_Hhp.csv')
    
    E_hp_list = []
    cols = ["Datetime", "Normalised number E_hp readings"]
    E_hp_df = pd.DataFrame(E_hp_list, columns = cols)
    E_hp_df.to_csv (r'C:\Users\jonat\GitKraken_Code\PHY346_NationalGrid_2019\sauce\number_readings_Ehp.csv')
    
    w_H = csv.writer(open("number_readings_Hhp.csv", "w"))
    for key, val in H_hp_count_dict.items():
        w_H.writerow([key, val])
        
    w_E = csv.writer(open("number_readings_Ehp.csv", "w"))
    for key, val in E_hp_count_dict.items():
        w_E.writerow([key, val])
    
    print("H_hp count: " , H_hp_count_dict)
    print("E_hp count: " ,E_hp_count_dict)
    return H_hp_count_dict , E_hp_count_dict

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



#    import pdb; pdb.set_trace()

#if __name__ == "__main__":
 #   main()