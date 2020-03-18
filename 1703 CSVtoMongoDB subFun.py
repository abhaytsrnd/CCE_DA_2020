def dtavalid (arg1,arg2): # arg1 is list of column names, arg2 is dataframe
    ColNames1  = arg1
    df1 = arg2   
    ColNames1 = arg1
    LenCol1 = len(ColNames1)
    ColTyp = []
    df1 = arg2
    LenDf1 = len(df1)
 
    # 15% rows checked for type of data in columns.
    QntytoChk = (round((15/100)*LenDf1 + 1))   #15% of rows checked but what if length > 10000     
    for NoofCol in range(LenCol1) :
        #print(ColNames[NoofCol])                                      #print line delete later
        NoofRwChkd = 0
        NoofStr = 0
        NoofNmr = 0
        randomlist = random.sample(range(0, LenDf1), QntytoChk)
        #print(randomlist)                                             #print line delete later
        while NoofRwChkd < QntytoChk :
            RwNo  = randomlist[NoofRwChkd]             
            if type(df1.iloc[RwNo,NoofCol]) == str :
                NoofStr += 1
            else : 
                NoofNmr += 1
            NoofRwChkd += 1
        if NoofStr > NoofNmr :
            ColTyp.append("Text")
        else :
            ColTyp.append("Numbers")
       
    Nopbl = True
    for noofcol in range(LenCol1) :
        NonStr = 0
        NonNmr = 0
        value = None                                     #  tried to check Nan entries against this. Did not work
        NoofNaN = 0
        PrblRCs = []
        for noofrw in range(LenDf1) :       #indentifying NaNs in entire column. How to identify individual cell with NaNs
            NoofNaN = sum(pd.isnull(df1[ColNames1[noofcol]]))
            if (ColTyp[noofcol] == "Text" and type(df1.iloc[noofrw,noofcol]) != str) :
                NonStr += 1
            if ColTyp[noofcol] == "Numbers" and type(df1.iloc[noofrw,noofcol]) == str :
                NonNmr += 1
            #elif df1.iloc[noofrw,noofcol] == value :     ## not working. Suggestions please for checking condition
            #     NoofNAN += 1
            
        
        if (NonNmr != 0 or NonStr != 0 or NoofNaN != 0) :
            Nopbl = False
            print("Column ",ColNames[noofcol]," should have only ",ColTyp[noofcol]+" but also contain")
            if ColTyp[noofcol] == "Text" :
                msg = (str(NonStr)+" Number of Non Strings. "+str(NoofNaN)+" Number of NaNs.")            
            if ColTyp[noofcol] == "Numbers" :
                msg = (str(NonNmr)+" Number of Non Numericals. "+str(NoofNaN)+" Number of NaNs.")

            
            print(msg,"\n\n")
    if Nopbl == False :
        print("The  columns are in database are  : ", ColNames1)     
        print("The corresponding types are       : ", ColTyp,)
        print("Total no of rows are " +str(LenDf1)+". \n")
        print("Issues found in columns mentioned above.")
        print("Issues created through line 23 of csvtomongodb.py. To stop make trblshoot = 'n'")
        print("Data cleaning to be done")
        #input("Please make note and press Enter key")
    return(Nopbl)
