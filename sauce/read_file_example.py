# -*- coding: utf-8 -*-
"""
Created on Mon Nov 25 14:21:39 2019

@author: jonat
"""
from datetime import datetime
import numpy as np
import pandas as pd
import os
import glob

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
           # if dt == datetime(2012, 12, 21, 17, 19):
            #    import pdb; pdb.set_trace()
    cols = ["Datetime", "H_hp", "temp", "wind", "precip"]
    data_df = pd.DataFrame(data_list, columns=cols)
    data_df.set_index("Datetime", inplace=True)
    return data_df
    
def main():
    file_path = "rhpp5103.csv"
    load_rhpp_csvs(file_path)

def indi_HP_table():
    data_list = []
    
    for filename in glob.glob('*.csv'):
        
        data_list_single = []
        with open(filename, "r") as fid:
            next(fid)
            lines = fid.readlines() # list of strings for lines in the file            
            for line in lines:
                row = line.strip("\n").split(",")
                dt = datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S")
                H_hp = np.nan if row[1] == "NA" else float(row[1])
                temp = np.nan if row[-3] == "NA" else float(row[-3])
                wind = np.nan if row[-1] == "NA" else float(row[-1])
                precip = np.nan if row[-2] == "NA" else float(row[-2])
                data_list_single.append([dt, H_hp, temp, wind, precip])
               # if dt == datetime(2012, 12, 21, 17, 19):
                #    import pdb; pdb.set_trace()
        cols = ["Datetime", "H_hp", "temp", "wind", "precip"]
        data_df = pd.DataFrame(data_list_single, columns=cols)
        data_df.set_index("Datetime", inplace=True)
    
        HPID = filename[4:8]
        start = data_df.index[0]
        end = data_df.index[-1]
        no_NA = data_df.H_hp.isna().sum()
        fraction_NA = no_NA / (data_df.H_hp.count() + no_NA)
        data_list.append([HPID, start, end, no_NA, fraction_NA])
    
    cols = ["HPID", "Start", "End", "#NA", "fraction_NA"]
    NA_data_df = pd.DataFrame(data_list,columns=cols)
    NA_data_df.set_index("HPID", inplace=True)
        
    print(NA_data_df)
    return(NA_data_df)
            
def number_readings():
    dict = {}
    
    for filename in glob.glob('*.csv'):
        
        with open(filename, "r") as fid:
            next(fid)
            lines = fid.readlines() # list of strings for lines in the file            
            for line in lines:
                row = line.strip("\n").split(",")
                dt = datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S")
                H_hp = np.nan if row[1] == "NA" else float(row[1])
        
        if dt not in dict:
            if dt.isna() == False:
                dict[dt] = 1
        else:
            if dt.isna() == False:
                dict[dt] += 1
    import pdb; pdb.set_trace()
                
    data_list = []
    
    


#    import pdb; pdb.set_trace()

#if __name__ == "__main__":
 #   main()