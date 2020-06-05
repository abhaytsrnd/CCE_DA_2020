# Import numpy and pandas packages 
import numpy as np
import pandas as pd  
import math as ma
import logging


class Team3onlineLinearRegression:

    def __init__(self, data, yval):
        logging.debug('log: Initialized Online Linear Regression!!')
        self.__predicts__ = [] 
        self.__params__ = [] 
        self.__stats__ = []
        self.__data__ = data
        self.__yval__ = yval
        for  i in range(len(data)):
            stats = {}
            self.__stats__.append(stats)
            #print("STATS id:",id(stats))
        stats1 = {}
        self.__stats__.append(stats1)
        #print("STATS id:",id(stats1))

    def predicts(self, data:[[float]]) -> [float]:
        logging.info("log: Online Linear Regression Model Predicts Invoked.")
        print('data', type(data), data)
        y_predicts = 0.0
        if(len(self.__data__) != len(data)):
            logging.error("logError: Number of Independent Variables Should be equal to " + str(len(self.__data__)))
            return y_predicts
        
        ####Calculate y predicts as per the solution
        y_cap = self.__params__[-1]
        for i in range (len(self.__params__)-1):
            #print ("i={0} j={1}".format(i,j))
            y_cap = y_cap + self.__params__[i]*data[i]
        y_predicts = float(round(y_cap,3))
        
        #print ("Y_Predicts are:", y_predicts)
        return y_predicts
        
        
    def fit(self):
        logging.info("log: Online Linear Regression Model Fit Invoked.")
        
        data = self.__data__
        yval = self.__yval__
        
        # Create Data Frame for the given data  
        
        #Create rows for the data frame
        num_data_points = len(yval)
        num_indep_vars = len(data)
        data4df = []
        for i in range(num_data_points):
            data_row_4df = []
            data_row_4df.append(yval[i])
            for j in range(num_indep_vars):
                data_row_4df.append(data[j][i])
            data4df.append(data_row_4df)
        #print(data_row_4df)
        
        #create column names for data frame
        ###Data Variable names
        data_var = []
        columns_4df = []
        columns_4df.append('y')
        data_var.append('y')
        data_var_indep = []
        for i in range(num_indep_vars):
            indep_var = 'x'+str(i+1)
            columns_4df.append(indep_var)
            data_var_indep.append(indep_var)
        data_var.append(data_var_indep)
    
        #print ("data_var:{0}".format(data_var))
    
        # Create the pandas DataFrame  
        df = pd.DataFrame(data4df, columns = columns_4df)
  
        # print dataframe.  
        #print(df) 
        
        arg1 = df
        arg2 = data_var
        
        ###For the stats
        minimum = {arg2[0]: round(arg1[arg2[0]].min(),3)}
        average = {arg2[0]: round(arg1[arg2[0]].mean(),3)}
        maximum = {arg2[0]: round(arg1[arg2[0]].max(),3)}      
        #print(average)
        i=0
        for ind_var in arg2[1]:
            average.update({arg2[1][i]: round(arg1[arg2[1][i]].mean(),3)})
            minimum.update({arg2[1][i]: round(arg1[arg2[1][i]].min(),3)})
            maximum.update({arg2[1][i]: round(arg1[arg2[1][i]].max(),3)})
            i=i+1
        #print("::Average::",average)
        #print("::minimum::",minimum)
        #print("::maximum::",maximum)
        ####Average
        
        
        ###Create new columns difference between avg and current value
        col_name = arg2[0]+str('-avg')
        #print(average[arg2[0]])
        arg1[col_name] =  (arg1[arg2[0]] - average[arg2[0]] )
        #print(arg1[col_name].sum()) ###To test if sum is zero.
        #print(arg1)

        i=0
        for ind_var in arg2[1]:
            col_name = ind_var+str('-avg')
            arg1[col_name] =  (arg1[arg2[1][i]] - average[arg2[1][i]] )
            #print(arg1[col_name].sum()) ###To test if sum is zero.
            i=i+1

        #print(arg1)


        ###Create new columns for square for (y-avg) 
        col_name = arg2[0]+str('-avg')
        new_col_name = str('sq-')+arg2[0]+str('-avg')
        #print(new_col_name)
        arg1[new_col_name] =  pow(arg1[col_name],2)

        #print(arg1)
        ###Create new columns for square for (x-avg) 
        i=0
        for ind_var in arg2[1]:
            col_name = ind_var+str('-avg')
            new_col_name = str('sq-')+ind_var+str('-avg')
            arg1[new_col_name] =  pow(arg1[col_name],2)

            i=i+1

        #print(arg1)


        ###Create new columns for dependent variable and independent variable (x-avg)(y-avg)
        dep_col_name = arg2[0]+str('-avg')
        #print("Dependent Column name:",dep_col_name)
        i=0
        for ind_var in arg2[1]:
            col_name = ind_var+str('-avg')
            new_col_name = '('+dep_col_name+')('+ind_var+str('-avg')+')'
            #print("Independent Column name:",col_name)
            #print("New Column name:",new_col_name)
            arg1[new_col_name] =  arg1[col_name]*arg1[dep_col_name]

            i=i+1

        #print(arg1)


        ####Calculating the correlation coefficients
        ####Calculating the covariance and Variance
        
        correlation_coefficients = {}
        all_covariance = {}
        all_variance = {}
        dep_col_name = arg2[0]+str('-avg')
        sq_dep_col_name = str('sq-')+arg2[0]+str('-avg')
        i=0
        for ind_var in arg2[1]:
            sq_in_col_name = str('sq-')+ind_var+str('-avg')
            in_de_col_name = '('+dep_col_name+')('+ind_var+str('-avg')+')'
            corr_coef = round(arg1[in_de_col_name].sum()/ma.sqrt(arg1[sq_in_col_name].sum()*arg1[sq_dep_col_name].sum()),3)
            correlation_coefficients[ind_var] = corr_coef
            #print ("For covariance: in_de_col_name:::",in_de_col_name)
            #print ("For covariance sum_of_squares: arg1[in_de_col_name].sum() :::",arg1[in_de_col_name].sum() )
            SampleSpace = len(arg1)
            #print ("For covariance SampleSpace::::",SampleSpace)
            if(SampleSpace <= 1):
               covariance = 0
               variance = 0
            else:
               covariance = round(((arg1[in_de_col_name].sum())/(SampleSpace-1)),3)
               variance = round(((arg1[sq_in_col_name].sum())/(SampleSpace-1)),3)
            all_covariance[ind_var] = covariance
            #print ("For variance: sq_in_col_name:::",sq_in_col_name)
            #print ("For variance sum_of_squares: arg1[sq_in_col_name].sum() :::",arg1[sq_in_col_name].sum() )
            #print ("For variance SampleSpace::::",SampleSpace)
            all_variance[ind_var] = variance
            i=i+1

        if(SampleSpace <= 1):
            covariance = variance = 0
        else:
            variance = covariance = round(((arg1[sq_dep_col_name].sum())/(SampleSpace-1)),3)
        all_variance[arg2[0]] = variance
        all_covariance[arg2[0]] = covariance
        #print("\nCorrelation Coefficients are: ",correlation_coefficients)
        #print("\All Covariance are: ",all_covariance)
        #print("\All Variance are: ",all_variance)
        #print("arg2 as passed in the function: ", arg2)


        ###update Stats from already populated Data
        for i in range(len(arg2[1])):
            stats = self.__stats__[i]
            #print("STATS id:",id(stats))
            stats["count"] = len(arg1)
            stats["mean"] = average[arg2[1][i]]
            stats["min"] = minimum[arg2[1][i]]
            stats["max"] = maximum[arg2[1][i]]
            stats["r"] = correlation_coefficients[arg2[1][i]]
            stats["variance"] = all_variance[arg2[1][i]]
            stats["covariance"] = all_covariance[arg2[1][i]]
            stats["std"] = round(ma.sqrt(all_variance[arg2[1][i]]),3)
            #print("STATS for X params:",stats)
            stats.update(stats)
        i=i+1
        stats1 = self.__stats__[i]
        #print("STATS for y id:",id(stats1))
        stats1["count"] = len(arg1)
        stats1["mean"] = average[arg2[0]]
        stats1["min"] = minimum[arg2[0]]
        stats1["max"] = maximum[arg2[0]]
        stats1["r"] = 1
        stats1["variance"] = all_variance[arg2[0]]
        stats1["covariance"] = all_covariance[arg2[0]]
        stats1["std"] = round(ma.sqrt(all_variance[arg2[0]]),3)
            
        #print("STATS for y:",stats1)
        stats1.update(stats1)

        


        ###Create new columns for all independent significant variables for ex Y1*X1
        rhs_matrix_col_names = []
        lhs_matrix_col_names = []


        for ind_var in arg2[1]:
            dep_indep_col_name = arg2[0]+str('*')+ind_var
            arg1[dep_indep_col_name] =  arg1[arg2[0]]*arg1[ind_var]
            ###store column names of rhs matrix
            rhs_matrix_col_names.append(dep_indep_col_name)
            #rhs_matrix_col_names.append(rhs_matrix_col_names_row)
        rhs_matrix_col_names.append(arg2[0])


        for ind_var in arg2[1]: 
            lhs_matrix_col_names_row = []
            for ind_var1 in arg2[1]:
                indep_indep_col_name = ind_var1+str('*')+ind_var
                arg1[indep_indep_col_name] =  arg1[ind_var1]*arg1[ind_var]
                ###store column names of lhs matrix
                lhs_matrix_col_names_row.append(indep_indep_col_name)                
            lhs_matrix_col_names_row.append(ind_var)
            lhs_matrix_col_names.append(lhs_matrix_col_names_row)

            
            
        #Adding last equation, 
        #Last variable is total sample space (N)
        lhs_matrix_col_names_row = []
        str1 = 'SS'
        for ind_var in arg2[1]: 
            lhs_matrix_col_names_row.append(ind_var)
        lhs_matrix_col_names_row.append(str1)
        lhs_matrix_col_names.append(lhs_matrix_col_names_row)

        #print(arg1)

        #print ("RHS Column names:", rhs_matrix_col_names)
        #print ("LHS Column names:", lhs_matrix_col_names)


        rhs_matrix = []
        lhs_matrix = []
        rhs_matrix_row = []


        i=0
        for item in rhs_matrix_col_names:
            #rhs_matrix_row.append(round(arg1[rhs_matrix_col_names[i]].sum(),2))
            #print("HERe is the data:",rhs_matrix_col_names[i])
            #rhs_matrix.append(rhs_matrix_row)
            rhs_matrix.append([round(arg1[rhs_matrix_col_names[i]].sum(),2)])
            i=i+1

        #print ("RHS Matrix:", rhs_matrix)



        for item in lhs_matrix_col_names:
            lhs_matrix_row = []
            #print("HERE IS ITEM::: item",item )
            for item1 in item:
                #print("HERE IS ITEM1::: item1",item1 )
                if(item1 == 'SS'):
                    lhs_matrix_row.append(round(arg1[arg2[0]].count(),2))
                #lhs_matrix_row.append(round(arg1[item1].sum(),2))
                #lhs_matrix.append(lhs_matrix_row)
                else:
                    lhs_matrix_row.append(round(arg1[item1].sum(),2))

            lhs_matrix.append(lhs_matrix_row)

        #print ("LHS Matrix:", lhs_matrix)



        ###NUMPY MAtrix creation

        RHS = np.array(rhs_matrix)
        LHS = np.array(lhs_matrix)
        #print("Matrix LHS is:\n",LHS)
        #print("Matrix RHS is:\n",RHS)

        #SOLVE THE EUATIONS using matrix inverse and multiplication
        LHS_inv = np.linalg.inv(LHS)
        #print("Inverse of Matrix LHS is:\n",LHS_inv)


        SOL = np.matmul(LHS_inv,RHS)
        #print("Solution of the equations are :\n",SOL)
        sol_list = SOL.tolist()
        sol_list1 = []
        #print("\nSolution of the equations are :\n",sol_list)

        for i in range (len(sol_list)):
            self.__params__.append(float(sol_list[i][0]))
            sol_list1.append(float(sol_list[i][0]))
        #print ("Solution-list:",sol_list1)


        ###Creating the Linear Regression Model
        linRegModel = []
        linRegModel = arg2[0]+str(' = ')
        i=0
        for ind_var in arg2[1]:
            if(i != 0):
                linRegModel = linRegModel + str(' + ')
            linRegModel = linRegModel + str(round(sol_list[i][0],3)) + str('*') + ind_var
            i=i+1

        linRegModel = linRegModel + str(' + ') + str(round(sol_list[-1][0],3))
        #print("\nTHE LINEAR REGRESSION MODEL is: ", linRegModel)
        #####


        ####Calculate y predicts as per the solution
        
        x_data = self.__data__
        
        for j in range(len(x_data[0])):
            y_cap = sol_list[-1][0]
            for i in range (len(sol_list)-1):
                #print ("i={0} j={1}".format(i,j))
                y_cap = y_cap + sol_list[i][0]*x_data[i][j]
            self.__predicts__.append(float(round(y_cap,3)))
        
        #print ("Y_Predicts are:", self.__predicts__)
        #print ("Y are:", self.__yval__)
        
        
        return (self.__params__, self.__stats__,self.__predicts__)
        
    

        #actual_params = [69.09484848484848, -117.14066666666645]
        #actual_stats = [{'count': 10, 'mean': 5.5, 'variance': 9.166666666666666, 'std': 3.0276503540974917, 'min': 1, 'max': 10, 'covariance': 633.3694444444444, 'r': 0.9617576489183196}, {'count': 10, 'mean': 262.881, 'variance': 47312.01869888888, 'std': 217.51326097249537, 'min': 7.5, 'max': 698.88, 'covariance': 47312.01869888888, 'r': 1}]
        #actual_ycap = [-48.045818181817964, 21.04903030303052, 90.143878787879, 159.2387272727275, 228.333575757576, 297.42842424242446, 366.5232727272729, 435.6181212121214, 504.71296969696994, 573.8078181818184]

        
        
#x = [1,2,3,4,5,6,7,8,9,10]
#y = [7.50,44.31,60.80,148.97,225.50,262.64,289.06,451.53,439.62,698.88]
#data = [x]
#model = OnlineLinearRegression(data,y)
#params, stats, y_predicts = model.fit(data, y)
#print ("Params",params)
#print ("Stats",stats)
#print ("y_predicts",y_predicts)
