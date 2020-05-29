# Team2 code for data cleaning
##############################################################
import pandas as pd
import numpy as np
import csv
import os
import random
import sys
#%whos

def data_cleaning(df) :

    LenDf = len(df)
    stats = {}

    ColNames  = []
    for Col in df.columns:
        ColNames.append(Col)
    LenCol = len(ColNames)

    ColTypes = IdenColTyp(df,LenDf,LenCol)  # for finding out type of data column wise.

    print("\nThe  columns in database are  : ", ColNames)
    print("The corresponding types are   : ", ColTypes)
    print("Total no of rows are          :  "+str(LenDf)+".")
    stats["col_name"] = ColNames
    stats["col_type"] = ColTypes
    stats["row_total"] = LenDf

    (proceed, FinDf, FinDfNoText, DFDefect) = DataValid(df,LenDf,ColNames,ColTypes,LenCol)      #  function for validating data

    for NoofCol in range(len(ColTypes)) :
        if ColTypes[NoofCol] == "Text":
            FinDfNoText = FinDfNoText.drop(columns=ColNames[NoofCol])

    stats["row_cleaned"] = len(FinDfNoText)
    stats["row_defect"] = len(DFDefect)
    return (FinDf, FinDfNoText, DFDefect, stats)

##############################################################
# 15% rows checked for identifying type of data in columns.
##############################################################
def IdenColTyp(arg1,arg2,arg3) :

    # arg1 is df
    # arg2 is LenDf
    # arg3 is LenCol
    #15% of rows checked but what if length > 10000
    perc = 1
    if(arg2) < 500 :
        perc = 1
    else :
        perc = 0.15

    if perc == 1 :
        QntytoChk = arg2
    elif ((round(perc)*arg2)%2) == 0 :          # To ensure odd number of rows selected for checking.
        QntytoChk = (round(perc)*arg2)+1
    else :
        QntytoChk = (round(perc)*arg2)

    ColTyp = []
    ColAvg = []
    for NoofCol in range(arg3) :
        NoofRwChkd = 0
        NoofStr = 0
        NoofNmr = 0
        randomlist = random.sample(range(0, arg2), QntytoChk)
        while NoofRwChkd < QntytoChk :
            RwNo  = randomlist[NoofRwChkd]
            CelVal = str(arg1.iloc[RwNo,NoofCol])
            NoofChar = 0
            NoofDig = 0
            # print(CelVal,'                Length is', len(CelVal))
            for i in range(len(CelVal)) :
                if CelVal != 'nan' :
                    if CelVal[i] !=  " " :
                        if CelVal[i] !=  "."  :
                            if CelVal[i].isalpha():
                                NoofChar += 1
                            if CelVal[i].isdigit() :
                                NoofDig +=1
            #print('Digits: ',NoofDig, 'Non Digits: ', NoofChar)
            if NoofChar > NoofDig :
                NoofStr += 1
            if NoofDig > NoofChar :
                NoofNmr += 1
            NoofRwChkd += 1
        #print(NoofStr,NoofNmr)
        #input("str   numeric")

        if NoofStr > NoofNmr :
            ColTyp.append("Text")
        else :
            ColTyp.append("Numbers")

    return(ColTyp)


#############################################################################
# checking for invalid entries(other than NaNs) in text and numeric columns
#############################################################################

def DataValid(arg1,arg2,arg3,arg4,arg5): # df,LenDf,ColNames,ColTypes,LenCol

    df1        = arg1
    LenDf1     = arg2
    ColNames1  = arg3
    ColTyp     = arg4
    LenCol1    = arg5
    #DFDefect = df1

    Nopbl = "True"
    DelRws = "N"
    NaNRC = []
    PrblRCs =[]
    #ColAvgVar =[[]]

    (TotNoNaN,TotRC) = Nandet(arg1,arg3,arg5)  # To get RC details of all NaNs.
    for noofcol in range(LenCol1) :
        NonStr = 0
        NonNmr = 0
        NoofNaN = sum(pd.isnull(df1[ColNames1[noofcol]]))   # summing number of Nan in each column.
        for noofrw in range(arg2) :
            if  ColTyp[noofcol] == "Text"  :
                CelVal = str(arg1.iloc[noofrw,noofcol])
                NoofChar = 0
                NoofDig = 0
                for i in range(len(CelVal)) :
                    if CelVal != 'nan' :
                        if CelVal[i] !=  " " :
                            if CelVal[i] !=  "."  :
                                if CelVal[i].isalpha():
                                    NoofChar += 1
                                if CelVal[i].isdigit() :
                                    NoofDig +=1
                if NoofChar == 0 :
                    NonStr += 1
                    TotRC.append([noofrw,noofcol])

            if ColTyp[noofcol] == "Numbers" :
                CelVal = str(df1.iloc[noofrw,noofcol])
                NoofChar = 0
                NoofDig = 0
                for i in range(len(CelVal)) :
                    if CelVal != 'nan' :
                        if CelVal[i] !=  " " :
                            if CelVal[i] !=  "."  :
                                if CelVal[i].isalpha():
                                    NoofChar += 1
                                if CelVal[i].isdigit() :
                                    NoofDig +=1
                if NoofChar > 0 :
                    NonNmr += 1
                    TotRC.append([noofrw,noofcol])

        if (NonNmr != 0 or NonStr != 0 or NoofNaN != 0) :
            Nopbl = "False"

    DFDefect1 = pd.DataFrame([])
    if Nopbl == "False" :
        (DFDefect1,Dellst) = BldDefDF(arg1,TotRC,arg3)  #Building a dataframe having where values are identified as invalid.
        df1 = df1.drop(Dellst,axis = 0)
        Nopbl = "True"
    return(Nopbl,df1,df1,DFDefect1)

#############################################################################
# for getting row and columns details of each NAN
#############################################################################
def Nandet(arg1,arg2,arg3) :  # df1,ColNames1;LenCol1

    TotNan = 0
    TotRC = []
    for ColNo in range(arg3) :
        ColSel = arg2[ColNo]
        NulRws  = (arg1[arg1[ColSel].isnull()].index.tolist())  #get Row nos for Nan in that Column
        NRLen = len(NulRws)
        for NoNul in range(NRLen) :
            TotNan += 1
            TotRC.append([NulRws[NoNul],ColNo])              #Create RC for the Nans in that Column
    #print(totNan,totRC)
    #input("enter")
    return(TotNan,TotRC)

#############################################################################
#Building a dataframe from original, where values are identified as invalid and a RC list created.
#############################################################################

def BldDefDF(arg1,arg2,arg3) :

    # arg1 df;
    # arg2 list of RCs  of original DF where data is identified as invalid or NaN
    # arg3 is list of Col names

    RLst = []                       # list containing 'R' values from list of RCs list
    for pshin in range(len(arg2)) :
        RLst.append(arg2[pshin][0])

    Compact_list = []               # After Removing Duplicates from Rlist
    for num in RLst:
        if num not in Compact_list:
            Compact_list.append(num)
    Compact_list.sort()

    DFDef = pd.DataFrame(columns = arg3)
    for itno in range(len(Compact_list)) :
        DFDef = DFDef.append(arg1.iloc[Compact_list[itno]])
    return(DFDef,Compact_list)
