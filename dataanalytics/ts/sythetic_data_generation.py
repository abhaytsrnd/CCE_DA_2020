
import os
import pandas as pd
import numpy as np
import datetime
from tkinter.filedialog import askopenfile
from tkinter import *
import tkinter as tk
from tkinter import ttk

# from math import sqrt
class MyWindow:
    def __init__(self, win):
        self.welcome = Label(win, text='Welcome To Synthetic Data Generation', font=('Helvetica', 20))
        self.note = Label(win, text='\n \n \n Note:', font=('Helvetica', 10))        
        self.note1 = Label(win, text='1. This module generates synthetic data using Thomas Fiering model which is applicable only for Stream Flow data ', font=('Helvetica', 10))        
        self.note2 = Label(win, text='2. This module generates data only at month level', font=('Helvetica', 10))        
        self.note3 = Label(win, text='3. Provide the input data in the format - [Date<dd/mm/yyyy>, Values]', font=('Helvetica', 10))        
        self.csv_in = Label(win, text='   Input csv file path   ', font=('Helvetica', 14))
        self.gen_years = Label(win, text='   Generate data for n years   ', font=('Helvetica', 14))
        self.entry_text = tk.StringVar()
        self.csv_in_entry = Entry(window, textvariable=self.entry_text, font=('Helvetica', 14))
        self.gen_years_entry = Entry(font=('Helvetica', 14))
        self.browse_but = Button(win, text='   Browse   ', command=lambda: self.open_file(), font=('Helvetica', 14))
        self.submit_but = Button(win, text='   Submit   ', command=lambda: self.get_data(), font=('Helvetica', 14))
        self.blank1 = Label(win, text='      ', font=('Helvetica', 14))
        self.blank2 = Label(win, text='      ', font=('Helvetica', 14))
        self.blank3 = Label(win, text='      ', font=('Helvetica', 14))
#        self.welcome.place(x=100, y=15)
#        self.csv_in.place(x=90, y=100)
#        self.gen_years.place(x=150, y=150)
#        self.csv_in_entry.place(x=200, y=100)
#        self.gen_years_entry.place(x=200, y=150)
#        self.browse_but.place(x=332, y=100)
#        self.submit_but.place(x=200, y=200)
#        self.t5.place(x=300, y=300)
        self.welcome.grid(row=1, columnspan=10)
        self.note.grid(row=9, columnspan=10, sticky = W)
        self.note1.grid(row=10, columnspan=10, sticky = W)
        self.note2.grid(row=11, columnspan=10, sticky = W)
        self.note3.grid(row=12, columnspan=10, sticky = W)
        self.csv_in.grid(row=3, column=0, sticky = E, columnspan = 1)
        self.gen_years.grid(row=4, column=0, sticky = E, columnspan = 1)
        self.csv_in_entry.grid(row=3, column=1, columnspan = 1)
        self.gen_years_entry.grid(row=4, column=1, columnspan = 1)
        self.browse_but.grid(row=3, column=4, columnspan = 1)
        self.submit_but.grid(row=6, column=1, columnspan = 1)
        self.blank1.grid(row=5, column=0, columnspan = 1)
        self.blank2.grid(row=2, column=0, columnspan = 1)
        self.blank3.grid(row=5, column=0, columnspan = 1)
#        self.blank.grid(row=2, column=2)
    def get_data(self):
        self.file_path = str(self.csv_in_entry.get())
        # self.sheet_name = str(self.t2.get())
        # self.column_index = str(self.t3.get())
        self.count = int(self.gen_years_entry.get())
        return self.gen_syn_data(self.file_path, self.count)
    def open_file(self):
        file = askopenfile(mode='r', filetypes=[('CSV Files', '*.csv')])
        self.entry_text.set(file.name)
    def gen_syn_data(self, file_name, count):
        waterFlow_day = pd.read_csv(file_name)
        waterFlow_day.columns = ['Date', 'WaterDischarge']
        waterFlow_day['Date'] = pd.to_datetime(waterFlow_day['Date'], format = '%d/%m/%Y')
        startDate = max(waterFlow_day.Date)
        no_of_years = int(count)
        # Generate the synthetic data skeleton dataframe
        generate_month_columns = waterFlow_day.columns
        generate_month  = pd.DataFrame(columns = generate_month_columns)
        generate_month['Date'] = pd.date_range(start = startDate, periods = (no_of_years * 12), freq = pd.offsets.MonthBegin(1))        
        waterFlow_day_new = pd.concat([waterFlow_day, generate_month])        
        waterFlow_day_new['Month'] = pd.DatetimeIndex(waterFlow_day_new.Date).month
        waterFlow_day_new['Year'] = pd.DatetimeIndex(waterFlow_day_new.Date).year
        # Aggregate the data from day level to Month Year level 
        waterFlow_month = waterFlow_day_new.groupby(['Year', 'Month']).agg('mean').reset_index()
        # Create an index column
        waterFlow_month = waterFlow_month.reset_index()        
        waterFlow_month['WaterDischarge_lag1'] = waterFlow_month['WaterDischarge'].shift(-1)
        waterFlow_month['WaterDischarge_lead1'] = waterFlow_month['WaterDischarge'].shift(1)
        # Create Training and Testing data
        train_test_split = (waterFlow_month.shape[0] - generate_month.shape[0]) - 1
        waterFlow_month_train = waterFlow_month[waterFlow_month['index'] <= train_test_split]
        waterFlow_month_test = waterFlow_month[waterFlow_month['index'] >= train_test_split]
        waterFlow_month_test = waterFlow_month_test.reset_index(drop=True)
        # Aggregate the data at month level using Training data
        waterFlow_month_train_agg = waterFlow_month_train.groupby('Month').agg({'WaterDischarge' : ['mean', 'std']})
        waterFlow_month_train_agg.columns = waterFlow_month_train_agg.columns.droplevel()
        waterFlow_month_train_agg = waterFlow_month_train_agg.reset_index()
        # Creating dataset for correlation
        max_year_index = int(waterFlow_month_train.shape[0]/12) * 12
        waterFlow_month_train_corr_ds = waterFlow_month_train[waterFlow_month_train['index'] < max_year_index]
        # Correlation calculation at month level (current month to next month)
        # Regression Coefficient calculation at month level
        for i in waterFlow_month_train_agg.Month.unique():
            if i == 1:
                j = 12
            else:
                j = i - 1
            waterFlow_month_train_agg.loc[waterFlow_month_train_agg['Month'] == i, 'corr'] = waterFlow_month_train_corr_ds[waterFlow_month_train_corr_ds['Month'] == i]['WaterDischarge'].reset_index()['WaterDischarge'].corr(waterFlow_month_train_corr_ds[waterFlow_month_train_corr_ds['Month'] == j]['WaterDischarge'].reset_index()['WaterDischarge'])
        #waterFlow_month_train[waterFlow_month_train['Month'] == i]['WaterDischarge'].reset_index()['WaterDischarge']
            waterFlow_month_train_agg.loc[waterFlow_month_train_agg['Month'] == i, 'reg_coeff'] = \
                waterFlow_month_train_agg[waterFlow_month_train_agg['Month'] == i]['corr'].item() \
                * (
                        waterFlow_month_train_agg[waterFlow_month_train_agg['Month'] == i]['std'].item() 
                        / waterFlow_month_train_agg[waterFlow_month_train_agg['Month'] == j]['std'].item()
                )
        del waterFlow_month_train_corr_ds
        # Generate Random Normal Deviate with zero mean and unit variance (Zt)
        mean=0
        variance=1
        rand_len = waterFlow_month_test.shape[0]
        rand_norm_deviate = np.random.normal(mean, variance, rand_len)
        waterFlow_month_test['rand_norm_deviate'] = pd.Series(rand_norm_deviate)
        # Synthetic Data Generation function
        train_agg = waterFlow_month_train_agg.copy()
        train_agg['corr_lag1'] = train_agg['corr'].shift(-1)
        train_agg['mean_lag1'] = train_agg['mean'].shift(-1)
        train_agg['corr_lag1'][11] = train_agg['corr'][0]
        train_agg['mean_lag1'][11] = train_agg['mean'][0]
        test_data_train_agg = waterFlow_month_test.merge(train_agg, on = 'Month')
        test_data_train_agg['sqrt'] = np.sqrt(1 - test_data_train_agg['corr_lag1']**2)
        index_min = test_data_train_agg['index'].unique().min()
        WaterDischarge_first = test_data_train_agg.loc[test_data_train_agg['index'] == index_min, 'WaterDischarge'].item()
        test_data_train_agg['WaterDischarge'] = np.nan
        test_data_train_agg.loc[test_data_train_agg['index'] == index_min, 'WaterDischarge'] = WaterDischarge_first
        test_loop_array = test_data_train_agg[test_data_train_agg['index'].unique() > index_min]
        for i in range(test_loop_array['index'].min(), test_loop_array['index'].max() + 1):
            #for i in test_loop_array['index'].unique():     
            test_data_train_agg.loc[test_data_train_agg['index'] == i, 'WaterDischarge'] = test_data_train_agg.loc[test_data_train_agg['index'] == i, 'mean'].item() \
                + (test_data_train_agg.loc[test_data_train_agg['index'] == i, 'reg_coeff'].item() \
                * (test_data_train_agg.loc[test_data_train_agg['index'] == (i - 1), 'WaterDischarge'].item() - test_data_train_agg.loc[test_data_train_agg['index'] == (i - 1), 'mean'].item()))   \
                + ( test_data_train_agg.loc[test_data_train_agg['index'] == i, 'rand_norm_deviate'].item() * test_data_train_agg.loc[test_data_train_agg['index'] == i, 'std'].item() \
                * test_data_train_agg.loc[test_data_train_agg['index'] == i, 'sqrt'].item())
        test_data_train_agg_subset = test_data_train_agg[['index', 'Year', 'Month', 'WaterDischarge',
                                                          'mean', 'std', 'corr', 'reg_coeff',
                                                          'rand_norm_deviate', 'corr_lag1', 'mean_lag1', 'sqrt']]
        # Replace the -ve values to 0
        for i in test_loop_array['index'].unique():        
        #    print(test_data_train_agg.loc[test_data_train_agg['index'] == i, 'gen_WaterDischarge'].item())
            if test_data_train_agg.loc[test_data_train_agg['index'] == i, 'WaterDischarge'].item() < 0:
                test_data_train_agg.loc[test_data_train_agg['index'] == i, 'WaterDischarge'] = 0
        waterFlow_month_test = test_data_train_agg[test_data_train_agg['index'] > index_min]
        waterFlow_month_test['WaterDischarge'] = waterFlow_month_test['WaterDischarge']
        waterFlow_month_test = waterFlow_month_test[['index', 'Year', 'Month', 'WaterDischarge']]
        ######################################################################################################################
        # Validation of generated data to training data
        ######################################################################################################################
        # Aggregate the data at month level using Training data
        waterFlow_month_test_agg = waterFlow_month_test.groupby('Month').agg({'WaterDischarge' : ['mean', 'std']})
        waterFlow_month_test_agg.columns = waterFlow_month_test_agg.columns.droplevel()
        waterFlow_month_test_agg = waterFlow_month_test_agg.reset_index()
        # Creating dataset for correlation
        min_year_index = (int(waterFlow_month_test['index'].min()/12) * 12) + 11
        max_year_index = (int(waterFlow_month_test['index'].max()/12) * 12)
        waterFlow_month_test_corr_ds = waterFlow_month_test[(waterFlow_month_test['index'] < max_year_index) & (waterFlow_month_test['index'] > min_year_index)]
        # Correlation calculation at month level (current month to next month)
        # Regression Coefficient calculation at month level
        for i in waterFlow_month_test_agg.Month.unique():
            if i == 1:
                j = 12
            else:
                j = i - 1
            waterFlow_month_test_agg.loc[waterFlow_month_test_agg['Month'] == i, 'corr'] = waterFlow_month_test_corr_ds[waterFlow_month_test_corr_ds['Month'] == i]['WaterDischarge'].reset_index()['WaterDischarge'].corr(waterFlow_month_test_corr_ds[waterFlow_month_test_corr_ds['Month'] == j]['WaterDischarge'].reset_index()['WaterDischarge'])
        #waterFlow_month_train[waterFlow_month_train['Month'] == i]['WaterDischarge'].reset_index()['WaterDischarge']
            waterFlow_month_test_agg.loc[waterFlow_month_test_agg['Month'] == i, 'reg_coeff'] = \
                waterFlow_month_test_agg[waterFlow_month_test_agg['Month'] == i]['corr'].item() \
                * (
                        waterFlow_month_test_agg[waterFlow_month_test_agg['Month'] == i]['std'].item() 
                        / waterFlow_month_test_agg[waterFlow_month_test_agg['Month'] == j]['std'].item()
                )
        waterFlow_month_final = pd.concat([waterFlow_month_train[['index', 'Year', 'Month', 'WaterDischarge']], 
                                           waterFlow_month_test[['index', 'Year', 'Month', 'WaterDischarge']]]).drop_duplicates()
        waterFlow_month_final['Date'] = pd.to_datetime(waterFlow_month_final[['Month', 'Year']].assign(DAY = 1))
        waterFlow_month_final = waterFlow_month_final[['Date', 'WaterDischarge']]
        agg_columns = ['Month', 'mean', 'std', 'corr']
        waterFlow_month_test_agg_display = waterFlow_month_test_agg[agg_columns].round(2)
        waterFlow_month_train_agg_display = waterFlow_month_train_agg[agg_columns].round(2)
        ######################################################################################################################
        # Final outputs
        ######################################################################################################################       
        new_window = Tk()
        new_window.minsize(600, 600)
        new_window.title('Synthetic Data Generation Results')
        #1 Final csv output comment with name
        waterFlow_month_final
        result_file = str(os.path.basename(file_name).split('.')[0])+'_with_synthetically_generated_data.csv'
        waterFlow_month_final.to_csv(result_file, index=False, header=True)
        # Print the message of csv stored
        csv_output_message = "Please find the csv file with synthetically generated data at \n \n <" + str(str(os.getcwd()) + os.sep + result_file) + ">"
        Label(new_window, text=csv_output_message, font=('Helvetica', 14)).grid(row = 8, column = 0, columnspan = 5)
#        q_lbl = Label(window, text=str(str(os.getcwd()) + os.sep + result_file), font=('Helvetica', 10))
        #Print given data > Start and End date
        waterFlow_month_train['Date'] = pd.to_datetime(waterFlow_month_train[['Month', 'Year']].assign(DAY = 1))
        print(waterFlow_month_train['Date'].min())
        print(waterFlow_month_train['Date'].max())    
        #Print generated data > Start and End date
        waterFlow_month_test['Date'] = pd.to_datetime(waterFlow_month_test[['Month', 'Year']].assign(DAY = 1))
        print(waterFlow_month_test['Date'].min())
        print(waterFlow_month_test['Date'].max())    
        #2 print(waterFlow_month_train_agg)
        print(waterFlow_month_train_agg)
        #3 print(waterFlow_month_test_agg)
        print(waterFlow_month_test_agg)
##############################################################################################
##############################################################################################
        # create Treeview with 3 columns        
        new_window.grid_rowconfigure(7, minsize = 50)
        new_window.grid_rowconfigure(9, minsize = 50)
#        Label(new_window , text='   Training dataset aggregates    ', font=('Helvetica', 14)).grid(row = 12, column = 0, columnspan = 4)
#        Label(new_window , text='   Testing dataset aggregates    ', font=('Helvetica', 14)).grid(row = 12, column = 4, columnspan = 4)
        Label(new_window , text='   Training dataset aggregates    ', font=('Helvetica', 14)).grid(row = 12, column = 0)
        Label(new_window , text='   Testing dataset aggregates    ', font=('Helvetica', 14)).grid(row = 12, column = 4)
        cols = tuple(agg_columns)
        trainbox = ttk.Treeview(new_window , columns=cols, show='headings')
        testbox = ttk.Treeview(new_window , columns=cols, show='headings')
        # set column headings
        for col in cols:
            trainbox.heading(col, text=col)
        trainbox.grid(row=13, column=0, columnspan=1, sticky = W)
        for col in cols:
            testbox.heading(col, text=col)    
        testbox.grid(row=13, column=4, columnspan=1)
        for i in range(len(waterFlow_month_train_agg_display)):
            trainbox.insert("", "end", values=(waterFlow_month_train_agg_display['Month'][i], 
                                               waterFlow_month_train_agg_display['mean'][i], 
                                               waterFlow_month_train_agg_display['std'][i], 
                                               waterFlow_month_train_agg_display['corr'][i]))
        for i in range(len(waterFlow_month_test_agg_display)):
            testbox.insert("", "end", values=(waterFlow_month_test_agg_display['Month'][i], 
                                               waterFlow_month_test_agg_display['mean'][i], 
                                               waterFlow_month_test_agg_display['std'][i], 
                                               waterFlow_month_test_agg_display['corr'][i]))
window = Tk()
window.minsize(600, 600)
mywin = MyWindow(window)
window.title('Synthetic Data Generation')
window.mainloop()
    
    
  
  

