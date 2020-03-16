import pandas as pd
import numpy as np
import pymongo
import json
import csv
import os

os.chdir(r'D:\DA_Project')               # change to directory containg working file
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
LinRegDB = myclient["LinReg"]            # DB for a group
LinRegIp = LinRegDB["LinReginput"]       # Collection 1 that is input file
LinREgOp = LinRegDB["LinRegoutput"]      # Collection 2 that is output file

delinp  = LinRegIp.delete_many({})       #  kept this for testing purposes
delout =  LinREgOp.delete_many({})       #  kept this for testing purposes
df=pd.read_csv("Automobiles_price_mileage_country.csv")   #  pass name of file thorugh user

ColNames  = []
for col in df.columns: 
    ColNames.append(col)
x = LinRegIp.delete_many({})    
for noofrw in range(len(df)) :
    rw = '{"_id" : ' + str(noofrw+1)
    for noofcol in range(len(ColNames)) :
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