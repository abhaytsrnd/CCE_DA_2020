import csv
import json
import pandas as pd
import sys, getopt, pprint
from pymongo import MongoClient
#CSV to JSON Conversion
csvfile = open('Automobiles_price_mileage_country.csv', 'r')
reader = csv.DictReader( csvfile )
mongo_client=MongoClient()
db=mongo_client.automobile_mileage
db.segment.drop()
header= [ "Make", "Country", "Mileage", "Price"]
print(reader)
for each in reader:
    row={}
    for field in header:
        row[field]=each[field]

    db.segment.insert(row)