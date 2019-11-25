# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
from datetime import date, time, datetime



    
date = pd.date_range(start= '1/1/2013', end = '1/1/2014', freq= '0h2min', )

DataFrame = {}
for key in DataFrame: 
    if date in DataFrame:
        date+=1
            

file = pd.read_csv("rhpp5103.csv")
file_NaN=file.isna()                #finds NaN values in panda dataframe
#import pdb; pdb.set_trace()
print(file_NaN)

#count no. NaN
NaN_count = file.loc[file.H_hp == 'NA', 'H_hp'].count()
print(NaN_count)
NaN_count = (file_NaN.H_hp == 'True').sum()
NaN_count = file_NaN.query('H_hp == "True"').H_hp.count()


#for loop - checks each csv to see if more than 10 NaN values
#for .csv in data:
   # if NaN_count > 10:
  #      print(NaN_count)
 #   else:
 #       skip
        
        
#add 1 to each time value in dataframe for count of no. csv's with a value for that time
#for "_.csv" in data:
   # i=0
    #for i in col:                    #iterate through each row
     #   if H_hp[i] =! 'NaN':         #if H_hp has a value
      #      count[i] in date += 1    #add 1 to the count col in the dataframe for the according time value
       # else:
        #    skip
        #i+=1
        