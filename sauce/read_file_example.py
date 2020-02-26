# -*- coding: utf-8 -*-
"""
Created on Mon Nov 25 14:21:39 2019

@author: jonat
"""
import numpy as np
import pandas as pd
from datetime import datetime

def main():
    file_path = "rhpp5103.csv"
    load_rhpp_csvs(file_path)
    return 

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
    return