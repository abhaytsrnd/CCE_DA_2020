# -*- coding: utf-8 -*-
"""
Created on Wed Jun  7 14:17:38 2017
@author: picku
"""


"""

Higer-Order Polynomial Bivariate Liner Regression

"""


import pandas as pd
import numpy as np
from scipy import linalg
from collections import OrderedDict
import matplotlib.pyplot as plt
from matplotlib import style
style.use('ggplot')

class PolynomialRegression(object):
        """PolynomialRegression 
        
        Parameters
        ------------
        x_pts : 1-d numpy array, shape = [n_samples,]
        y_pts : 1-d numpy array, shape = [n_samples,]
    
        
        Attributes
        ------------
        theta : 1-d numpy array, shape = [polynomial order + 1,] 
            Ceofficients of fitted polynomial, with theta[0] corresponding
            to the intercept term        
        
        method : str , values = 'normal_equation' 
            Method used for finding optimal values of theta
                    
        References
        ------------
        https://en.wikipedia.org/wiki/Polynomial_regression
        """

        def __init__(self, x, y):     
            
            self.x = x
            self.y = y      
    
        def standardize(self,data):
            """ Peform feature scaling
            Parameters:
            ------------
            data : numpy-array, shape = [n_samples,]
            
            Returns:
            ---------
            Standardized data                  
            """
    
            return (data - np.mean(data))/(np.max(data) - np.min(data))
            
        def hypothesis(self, theta, x):
            """ Compute hypothesis, h, where
            h(x) = theta_0*(x_1**0) + theta_1*(x_1**1) + ...+ theta_n*(x_1 ** n)
            Parameters:
            ------------
            theta : numpy-array, shape = [polynomial order + 1,]        
            x : numpy-array, shape = [n_samples,]
            
            Returns:
            ---------
            h(x) given theta values and the training data
            """       
            h = theta[0]
            for i in np.arange(1, len(theta)):
                h += theta[i]*x ** i        
            return h        
            
        def computeCost(self, x, y, theta):
            """ Compute value of cost function J 
            
            Parameters:
            ------------
            x : numpy array, shape = [n_samples,]
            y : numpy array, shape = [n_samples,]
            
            Returns:
            ---------
            Value of cost function J at value theta given the training data
            
            """    
            m = len(y)  
            h = self.hypothesis(theta, x)
            errors = h-y
            
            return (1/(2*m))*np.sum(errors**2) 
            
        def fit(self, method = 'normal_equation', order = 1):
            
            """Fit theta to the training data
            
            Parameters
            -----------
            method: string, values = 'normal_equation'
                 Indicates method for which polynomial regression will be performed
                
            order: int, optional
                 Order of polynomial fit. Defaults to 1 (linear fit)
                                 
            Returns:
            -----------
            self : object
            
            """
            d = {}    
            
            d['x' + str(0)] = np.ones([1,len(self.x)])[0]    
            for i in np.arange(1, order+1):                
                d['x' + str(i)] = self.x ** (i)        
                
            d = OrderedDict(sorted(d.items(), key=lambda t: t[0]))
            
            X = np.column_stack(d.values())  
            
            theta = np.matmul(np.matmul(linalg.pinv(np.matmul(np.transpose(X),X)), np.transpose(X)), self.y)

            self.method = method    
            self.theta = theta        
            self.d = d
            return self
            
        def plot_predictedPolyLine(self):
            """Plot predicted polynomial line using values of theta found
            using normal equation
            
            Returns
            -----------       
            matploblib figure
            """        
            plt.figure()
            plt.scatter(self.x, self.y, s = 30, c = 'b') 
            line = self.theta[0] #y-intercept 
            label_holder = []
            label_holder.append('%.*f' % (2, self.theta[0]))
            for i in np.arange(1, len(self.theta)):            
                line += self.theta[i] * self.x ** i 
                label_holder.append(' + ' +'%.*f' % (2, self.theta[i]) + r'$x^' + str(i) + '$') 
    
            plt.plot(self.x, line, label = ''.join(label_holder))        
            plt.title('Polynomial Fit: Order ' + str(len(self.theta)-1))
            plt.xlabel('x')
            plt.ylabel('y') 
            plt.legend(loc = 'best')      
    

def polynomialEquationConstructor(x_pts, y_pts, equation_order):
    
    """ separating the dependent and independent variable from the data"""
    #x_pts = data[str(X)]
    #y_pts = data[str(Y)]
    
    """ Initializing the object to perform the regression"""
    PR = PolynomialRegression(x_pts, y_pts)
    
    """ The line is fitterfor the given equation"""
    PR.fit(method = 'normal_equation', order = equation_order)
    #PR.plot_predictedPolyLine()
    
    """ Documenting the required output"""
    fitted_line_dict = PR.d
    fitted_line = fitted_line_dict[list(fitted_line_dict.keys())[-1]]
    theta_variables = PR.theta
    method = PR.method
    
    return fitted_line, theta_variables, method 



"""
# Reading the testing data set
data = pd.read_csv("C:/Users/VDinesh.Kumar/Desktop/Mamamiyaaaaaa/IISC/Project/" + "test_data_set.csv")
equation_order = 3

fitted_line, theta_variables, equation_order, method  = polynomialEquationConstructor(data, data.columns[0], data.columns[1], equation_order)

print("actual_line :", data['y'])
print("="*40)
print("fitted_line :", fitted_line)
print("="*40)
print("theta_variables :", theta_variables)
print("="*40)
print("equation_order :", equation_order)
print("="*40)
print("method :", method)
print("="*40)

"""