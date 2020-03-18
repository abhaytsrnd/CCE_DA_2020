#csvtomongodb.py

import pandas as pd
import numpy as np
import pymongo
import json
import csv
import os
import random

os.chdir(r'D:\CCE_DA_Project')           # change to directory containg working file
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
LinRegDB = myclient["LinReg"]            # DB for a group
LinRegIp = LinRegDB["LinReginput"]       # Collection 1 input file
LinREgOp = LinRegDB["LinRegoutput"]      # Collection 2 Results. (single or multiple for different groups)

delinp  = LinRegIp.delete_many({})       #  kept this for testing purposes
delout =  LinREgOp.delete_many({})       #  kept this for testing purposes
df=pd.read_csv("Automobiles_price_mileage_country.csv")   #  pass name of file thorugh user
LenDf = len(df)

# To be  deleted. Presently for testing
trblshoot = 'y'
if trblshoot == "y" :                        
    df.iloc[0,0] = 1                            # changing entry to  numeric in char col to test
    df.iloc[14,1] = 1                           # changing entry to  numeric in char col to test
    df.iloc[33,2] = "a"                         # changing entry to  char in numeric col to test
    df.iloc[41,3] = "a"                         # changing entry to  char in numeric col to test
    tempn = df.iloc[2,3]                        # to be delted after being able to change nan to valid data through a function
    df.iloc[2,3] = np.nan                       # changing entry to nan in  col 3
    tempn1 = df.iloc[6,1]                       # to be delted after being able to change nan to valid data through a function
    df.iloc[6,1] = np.nan                       # changing entry to nan in  col 1
    
    
ColNames  = []
for col in df.columns: 
    ColNames.append(col)
LenCol = len(ColNames)

proceed = dtavalid(ColNames,df)      #  function for validating data

df.iloc[2,3] = tempn                   # to be delted after being able to change nan to valid data through a function
df.iloc[6,1] = tempn1                  # to be delted after being able to change nan to valid data through a function
if proceed == True :
    for noofrw in range(LenDf) :
        rw = '{"_id" : ' + str(noofrw+1)
        for noofcol in range(LenCol) :
            rw = rw+', "'+ColNames[noofcol]+'": '
            if type(df.iloc[noofrw,noofcol]) == str :
                rw = rw+'"'+(df.iloc[noofrw,noofcol])+'"'    #  to put quotes if data is a string
            else :                                        
                rw = rw+str(df.iloc[noofrw,noofcol])         # not putting quotes if not a string
        rw = rw+' }'
        rwdict = json.loads(rw)
        x = LinRegIp.insert_one(rwdict)

    for x in LinRegIp.find():
        print(x)
    print(type(LinRegIp))
