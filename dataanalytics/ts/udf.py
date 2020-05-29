#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 22 23:41:14 2020

@author: z087322
"""



import numpy as np
from linear_regression import LinearRegression
from statistics import Statistics
import matplotlib.pyplot as plt
import math
#import matplotlib.pylab as plt
#from pylab import rcParams

def shift(ip, n):
    op = np.empty_like(ip)
    if n >= 0:
        op[:n] = np.nan
        op[n:] = ip[:-n]
    else:
        op[n:] = np.nan
        op[:n] = ip[-n:]
    return op

def pcf_data(ip, n):
    op_list = []
    for i in range(1, n+1):
        lag_op = shift(ip, i)
        op_tmp = list(Statistics.covariance(ip[i:], lag_op[i:]))
        op_list.append([i, op_tmp[1]])
    return op_list 

def create_bar_plot(x_col, y_col, x_label,
                    y_label, graph_title, subplot_n
                    , start, end, row_span, col_span, 
                    ts_len = None, lag_n = 25):
    subplot_n = plt.subplot2grid(start, end, rowspan=row_span, colspan=col_span)
    subplot_n.bar(x_col, y_col)
    if ts_len != None:
        tmp_val = 1.96/math.sqrt(ts_len)
        subplot_n.plot([1, lag_n], [tmp_val, tmp_val], color = '#444444', linestyle = "--")
        subplot_n.plot([1, lag_n], [-tmp_val, -tmp_val], color = '#444444', linestyle = "--")
    subplot_n.set_xlabel(x_label)
    subplot_n.set_ylabel(y_label)
    subplot_n.set_title(graph_title)
    
def lag_diff(ip, lag_n):
    lag_op = shift(ip, lag_n)
    op_list = ip[lag_n:] - lag_op[lag_n:]
    return op_list

def pq_param(acf_pacf_df, ts_len):
    tmp_val = 1.96/math.sqrt(ts_len)
    acf_pacf_df['acf_sig'] = acf_pacf_df['acf'].apply(lambda x: 1 if ((x >= tmp_val) or (x <= -tmp_val)) else 0)
    acf_pacf_df['pacf_sig'] = acf_pacf_df['pacf'].apply(lambda x: 1 if ((x >= tmp_val) or (x <= -tmp_val)) else 0)
    p = acf_pacf_df[acf_pacf_df['pacf_sig'] == 1].max()['lag']
    q = acf_pacf_df[acf_pacf_df['acf_sig'] == 1].max()['lag']
    return max(0,p), max(0, q)


#un-used function
def create_line_plot(x_col, y_col, plot_color, plot_style, 
                     x_label, y_label, graph_title, subplot_n
                     , start, end, row_span, col_span):
    subplot_n = plt.subplot2grid(start, end, rowspan=row_span, colspan=col_span)
    subplot_n.plot(x_col, y_col, color = plot_color, linestyle = plot_style)
    subplot_n.set_xlabel(x_label)
    subplot_n.set_ylabel(y_label)
    subplot_n.set_title(graph_title)


def AR_coef(y_lst, p):
    tmp_p=1
    tmp_lag_data = []
    while tmp_p<=p:
        tmp_op = shift(y_lst, tmp_p)
        tmp_lag_data.append(tmp_op)
        tmp_p+=1
    y_var = y_lst
    x_var = [list(x) for x in zip(*tmp_lag_data)]
    AR_res = LinearRegression.fit( x_var[p:], y_var[p:])
    return AR_res


'''
tmp_ip = list(diff_ip_ts)
x = AR_coef(tmp_ip, 4)


import lib.linear_regression
import numpy as np

tmp_p=1
p=4
tmp_lag_data = []
y_lst = list(diff_ip_ts)
while tmp_p<=p:
    tmp_op = shift(y_lst, tmp_p)
    tmp_lag_data.append(tmp_op)
    tmp_p+=1
y_var = y_lst
x_var = [list(x) for x in zip(*tmp_lag_data)]

x_var_array = np.asarray(x_var[p:])
y_var_array = np.asarray(y_lst)

AR_res = lib.linear_regression.LinearRegression.fit(x_var[p:], y_var[p:], tmp_lag_data[p:])

AR_res = lib.linear_regression.LinearRegression.fit(x_var_array, y_var_array, y_var_array)     
   ''' 
    

    