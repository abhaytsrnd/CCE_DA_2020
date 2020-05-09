# Team2 code for data cleaning
##############################################################
import random
import pandas as pd
import numpy as np

def data_cleaning(df):
    print("Team2 data cleaning API called")
    ColNames=[]
    for Col in df.columns:
        ColNames.append(Col)
    LenCol = len(ColNames)
    LenDf = len(df)
    ColTypes = IdenColTyp(df,LenDf,LenCol)  # for finding out type of data column wise.

    print("\nThe  columns in database are  : ", ColNames)     
    print("The corresponding types are   : ", ColTypes)
    print("Total no of rows are          :  "+str(LenDf)+". \n")
    
    (proceed,FinDf) = DataValid(df,LenDf,ColNames,ColTypes,LenCol)      #  function for validating data
    
    return FinDf

##############################################################
# 15% rows checked for identifying type of data in columns. 
##############################################################
def IdenColTyp(arg1,arg2,arg3) : 
  
    # arg1 is df
    # arg2 is LenDf
    # arg3 is LenCol
    #15% of rows checked but what if length > 10000  
    
    if ((round(15/100)*arg2)%2) == 0 :          # To ensure odd number of rows selected for checking.
        QntytoChk = (round(15/100)*arg2)+1
    else :
        QntytoChk = (round(15/100)*arg2)
        
    ColTyp = []
    ColAvg = []
    for NoofCol in range(arg3) :
        NoofRwChkd = 0
        NoofStr = 0
        NoofNmr = 0
        randomlist = random.sample(range(0, arg2), QntytoChk)
        while NoofRwChkd < QntytoChk :
            RwNo  = randomlist[NoofRwChkd]             
            if type(arg1.iloc[RwNo,NoofCol]) == str :
                NoofStr += 1
            else : 
                NoofNmr += 1
            NoofRwChkd += 1
        if NoofStr > NoofNmr :
            ColTyp.append("Text")
        else :
            ColTyp.append("Numbers")
            
    return(ColTyp)
    
#############################################################################
# checking for invalid entries(other than NaNs) in text and numeric columns 
#############################################################################
def DataValid (arg1,arg2,arg3,arg4,arg5): # df,LenDf,ColNames,ColTypes,LenCol
     
    df1        = arg1   
    LenDf1     = arg2
    ColNames1  = arg3
    ColTyp     = arg4
    LenCol1    = arg5

    Nopbl = "True"
    DelRws = "N"
    NaNRC = []
    PrblRCs =[]
    ColAvgVar =[[]]
    
    (TotNoNaN,TotRC) = Nandet(arg1,arg3,arg5)  # To get RC details of all NaNs.
    
    for noofcol in range(arg5) :
        ColValidNos = []
        NonStr = 0
        NonNmr = 0  
        NoofNaN = sum(pd.isnull(df1[ColNames1[noofcol]]))   # summing number of Nan in each column.
        for noofrw in range(arg2) :            
            if (ColTyp[noofcol] == "Text" and type(arg1.iloc[noofrw,noofcol]) != str ) :
                NonStr += 1
                TotRC.append([noofrw,noofcol])
                
            if ColTyp[noofcol] == "Numbers" :
                if type(df1.iloc[noofrw,noofcol]) != str :
                    ColValidNos.append(df1.iloc[noofrw,noofcol])
                if type(df1.iloc[noofrw,noofcol]) == str :
                    NonNmr += 1
                    TotRC.append([noofrw,noofcol])
                
        if ColTyp[noofcol] == "Numbers" :
            ColValidNos1 =[]
            for noc in range(len(ColValidNos)):
                if ~np.isnan(ColValidNos[noc]) :
                    ColValidNos1.append(ColValidNos[noc])
            ColAvgVar = varf(ColValidNos1)
            
        if (NonNmr != 0 or NonStr != 0 or NoofNaN != 0) :
            Nopbl = "False"
            print("Column ",ColNames[noofcol]," should have only ",ColTyp[noofcol]+" but also contains")
            if ColTyp[noofcol] == "Text" :
                msg = (str(NonStr)+" Number of Non Strings of which "+str(NoofNaN)+" are NaNs.")            
            if ColTyp[noofcol] == "Numbers" :
                msg = (str(NonNmr)+" Number of Non Numericals and "+str(NoofNaN)+" Number of NaNs.\nMean, Variance and Std Deviation of Valid entries in this column are "+"%.3f" %ColAvgVar[0]+"  "+"%.3f" %ColAvgVar[1]+" "+"%.3f" %math.sqrt(ColAvgVar[1]))

            print(msg,'\n')
            
    if Nopbl == "False" :
        (DFDefect,Dellst) = BldDefDF(arg1,TotRC,arg3)  #Building a dataframe having where values are identified as invalid.
        print("Total Number of NaNs are :",TotNoNaN,'.  Also check for other wrong entries as mentioned above. \n')
        print("Following is the list of rows where data is not valid and has to be corrected.\nNo of defective rows presented",len(DFDefect),"of ",LenDf1,"which is ","%.2f" %(len(DFDefect)*100/LenDf1),"%.\n\n")
        print(DFDefect)
        print("\nOnly defective data presented above. Complete including defective data given below, which could guide in rectifying\n")
        print(df1)
        DelRws = input("Please go throuh the above data. Enter y to delete rows with defective data and proceed to prepare MongoDB. \nWARNING !!!!!  Above mentioned % of data will be deleted !!!!!\n")    
        
    if DelRws.upper() == "Y" :
        df1 = df1.drop(Dellst,axis = 0)
        Nopbl = "True"
        
    return(Nopbl,df1)
    
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
    
#############################################################################
def varf (arg1): # Array of numbers to be passed
    if len(arg1) == 0:
        return("Array is empty")
    meanv = meanf(arg1)
    sqdsumdiff = 0
    for number in range(len(arg1)):
        sqdsumdiff += (arg1[number]-meanv)*(arg1[number]-meanv)
        var = sqdsumdiff/(len(arg1)-1)
    return (meanv,var)  # unpack this output tuple for extracting meanv and Var after storing this in any variable eg. z (Mean, Variance) = z
    
#############################################################################
def meanf (arg1): # Array of numbers to be passed
    if len(arg1) == 0:
        return("Array is empty")
    sumarg1 = 0
    for number in range(len(arg1)):
        sumarg1 += arg1[number]
        Avg = sumarg1/len(arg1)
    return(Avg)