import os

import pandas as pd
import numpy as np
import datetime
from tkinter.filedialog import askopenfile
from tkinter import *
import tkinter as tk

# from math import sqrt
class MyWindow:
    def __init__(self, win):
        self.lbl0 = Label(win, text='Welcome To Synthetic Data Generation', font=('Verdana', 20))
        self.lbl1 = Label(win, text='Input CSV file path')
        self.lbl4 = Label(win, text='Count')
        self.entry_text = tk.StringVar()
        self.t1 = Entry(window, textvariable=self.entry_text)
        self.t4 = Entry()
        self.b1 = Button(win, text='Browse', command=lambda: self.open_file())
        self.b2 = Button(win, text='Submit', command=lambda: self.get_data())
        self.lbl0.place(x=100, y=15)
        self.lbl1.place(x=90, y=100)
        self.lbl4.place(x=150, y=150)
        self.t1.place(x=200, y=100)
        self.t4.place(x=200, y=150)
        self.b1.place(x=332, y=100)
        self.b2.place(x=200, y=200)

    def get_data(self):
        self.file_path = str(self.t1.get())
        # self.sheet_name = str(self.t2.get())
        # self.column_index = str(self.t3.get())
        self.count = int(self.t4.get())
        return self.gen_syn_data(self.file_path, self.count)

    def open_file(self):
        file = askopenfile(mode='r', filetypes=[('CSV Files', '*.csv')])
        self.entry_text.set(file.name)

    def gen_syn_data(self, file_name, count):
        waterFlow_day = pd.read_csv(file_name)
        waterFlow_day['Date'] = pd.to_datetime(waterFlow_day['Date'], format='%d/%m/%Y')

        startDate = max(waterFlow_day.Date)
        no_of_years = int(count)

        # Generate the synthetic data for the 20 years
        generate_month_columns = waterFlow_day.columns
        generate_month = pd.DataFrame(columns=generate_month_columns)
        generate_month['Date'] = pd.date_range(start=startDate, periods=(no_of_years * 12),
                                               freq=pd.offsets.MonthBegin(1))

        waterFlow_day_new = pd.concat([waterFlow_day, generate_month])

        waterFlow_day_new['Month'] = pd.DatetimeIndex(waterFlow_day_new.Date).month
        waterFlow_day_new['Year'] = pd.DatetimeIndex(waterFlow_day_new.Date).year

        # Aggregate the data from day level to Month Year level
        waterFlow_month = waterFlow_day_new.groupby(['Year', 'Month']).agg('sum').reset_index()
        # Create an index column
        waterFlow_month = waterFlow_month.reset_index()

        waterFlow_month['WaterDischarge_lag1'] = waterFlow_month['WaterDischarge'].shift(-1)
        waterFlow_month['WaterDischarge_lead1'] = waterFlow_month['WaterDischarge'].shift(1)

        # Create Training and Testing data
        train_test_split = (waterFlow_month.shape[0] - generate_month.shape[0]) - 1
        waterFlow_month_train = waterFlow_month[waterFlow_month['index'] <= train_test_split]
        waterFlow_month_test = waterFlow_month[waterFlow_month['index'] >= train_test_split]

        # Aggregate the data at month level using Training data
        waterFlow_month_train_agg = waterFlow_month_train.groupby('Month').agg({'WaterDischarge': ['mean', 'std']})
        waterFlow_month_train_agg.columns = waterFlow_month_train_agg.columns.droplevel()
        waterFlow_month_train_agg = waterFlow_month_train_agg.reset_index()

        # Correlation calculation at month level (current month to next month)
        waterFlow_month_train_agg['corr'] = np.nan
        for i in waterFlow_month_train.Month.unique():
            waterFlow_month_train_agg.loc[waterFlow_month_train_agg['Month'] == i, 'corr'] = \
                waterFlow_month_train[waterFlow_month_train['Month'] == i]['WaterDischarge'].corr(
                    waterFlow_month_train['WaterDischarge_lag1'])

        # Regression Coefficient calculation at month level
        waterFlow_month_train_agg['reg_coeff'] = np.nan

        for i in waterFlow_month_train_agg.Month.unique():
            if i == 1:
                j = 12
            else:
                j = i - 1

            waterFlow_month_train_agg.loc[waterFlow_month_train_agg['Month'] == i, 'reg_coeff'] = \
                waterFlow_month_train_agg[waterFlow_month_train_agg['Month'] == i]['corr'].item() \
                * (
                        waterFlow_month_train_agg[waterFlow_month_train_agg['Month'] == i]['std'].item()
                        / waterFlow_month_train_agg[waterFlow_month_train_agg['Month'] == j]['std'].item()
                )

        # Generate Random Normal Deviate with zero mean and unit variance (Zt)
        mean = 0
        variance = 1
        rand_norm_deviate = np.random.normal(mean, variance, 12)
        waterFlow_month_train_agg['rand_norm_deviate'] = pd.Series(rand_norm_deviate)

        # Synthetic Data Generation function
        train_agg = waterFlow_month_train_agg.copy()

        # test_data = waterFlow_month_test.copy()

        train_agg['corr_lag1'] = train_agg['corr'].shift(-1)
        train_agg['mean_lag1'] = train_agg['mean'].shift(-1)

        train_agg['corr_lag1'][11] = train_agg['corr'][0]
        train_agg['mean_lag1'][11] = train_agg['mean'][0]

        test_data_train_agg = waterFlow_month_test.merge(train_agg, on='Month')
        test_data_train_agg['sqrt'] = np.sqrt(1 - test_data_train_agg['corr_lag1'] ** 2)

        index_min = test_data_train_agg['index'].unique().min()
        WaterDischarge_first = test_data_train_agg.loc[
            test_data_train_agg['index'] == index_min, 'WaterDischarge'].item()
        test_data_train_agg['WaterDischarge'] = np.nan
        test_data_train_agg.loc[test_data_train_agg['index'] == index_min, 'WaterDischarge'] = WaterDischarge_first
        test_loop_array = test_data_train_agg[test_data_train_agg['index'].unique() > index_min]
        for i in range(test_loop_array['index'].min(), test_loop_array['index'].max() + 1):
            # for i in test_loop_array['index'].unique():
            test_data_train_agg.loc[test_data_train_agg['index'] == i, 'WaterDischarge'] = test_data_train_agg.loc[
                                                                                               test_data_train_agg[
                                                                                                   'index'] == i, 'mean'].item() \
                                                                                           + (test_data_train_agg.loc[
                                                                                                  test_data_train_agg[
                                                                                                      'index'] == i, 'reg_coeff'].item() \
                                                                                              * (
                                                                                                          test_data_train_agg.loc[
                                                                                                              test_data_train_agg[
                                                                                                                  'index'] == (
                                                                                                                          i - 1), 'WaterDischarge'].item() -
                                                                                                          test_data_train_agg.loc[
                                                                                                              test_data_train_agg[
                                                                                                                  'index'] == (
                                                                                                                          i - 1), 'mean'].item())) \
                                                                                           + (test_data_train_agg.loc[
                                                                                                  test_data_train_agg[
                                                                                                      'index'] == i, 'rand_norm_deviate'].item() *
                                                                                              test_data_train_agg.loc[
                                                                                                  test_data_train_agg[
                                                                                                      'index'] == i, 'std'].item() \
                                                                                              * test_data_train_agg.loc[
                                                                                                  test_data_train_agg[
                                                                                                      'index'] == i, 'sqrt'].item())
            test_data_train_agg.loc[test_data_train_agg['index'] == i, 'part1_mean'] = test_data_train_agg.loc[
                test_data_train_agg['index'] == i, 'mean'].item()

            test_data_train_agg.loc[test_data_train_agg['index'] == i, 'part2'] = (
                        test_data_train_agg.loc[test_data_train_agg['index'] == i, 'reg_coeff'].item() \
                        * (test_data_train_agg.loc[test_data_train_agg['index'] == (i - 1), 'WaterDischarge'].item() -
                           test_data_train_agg.loc[test_data_train_agg['index'] == (i - 1), 'mean'].item()))
            test_data_train_agg.loc[test_data_train_agg['index'] == i, 'part2_reg_coeff'] = test_data_train_agg.loc[
                test_data_train_agg['index'] == i, 'reg_coeff'].item()

            test_data_train_agg.loc[test_data_train_agg['index'] == i, 'part2_diff'] = test_data_train_agg.loc[
                                                                                           test_data_train_agg[
                                                                                               'index'] == (
                                                                                                       i - 1), 'WaterDischarge'].item() - \
                                                                                       test_data_train_agg.loc[
                                                                                           test_data_train_agg[
                                                                                               'index'] == (
                                                                                                       i - 1), 'mean'].item()
            test_data_train_agg.loc[test_data_train_agg['index'] == i, 'part2_diff1'] = test_data_train_agg.loc[
                test_data_train_agg['index'] == (i - 1), 'WaterDischarge'].item()
            test_data_train_agg.loc[test_data_train_agg['index'] == i, 'part2_diff2'] = test_data_train_agg.loc[
                test_data_train_agg['index'] == (i - 1), 'mean'].item()

            test_data_train_agg.loc[test_data_train_agg['index'] == i, 'part3'] = (
                        test_data_train_agg.loc[test_data_train_agg['index'] == i, 'rand_norm_deviate'].item() *
                        test_data_train_agg.loc[test_data_train_agg['index'] == i, 'std'].item() \
                        * test_data_train_agg.loc[test_data_train_agg['index'] == i, 'sqrt'].item())
        test_data_train_agg_subset = test_data_train_agg[
            ['index', 'Year', 'Month', 'WaterDischarge', 'part1_mean', 'part2', 'part2_reg_coeff', 'part2_diff',
             'part2_diff1', 'part2_diff2', 'part3', 'mean', 'std', 'corr', 'reg_coeff', 'rand_norm_deviate',
             'corr_lag1', 'mean_lag1', 'sqrt']]

        # Replace the -ve values to 0
        for i in test_loop_array['index'].unique():
            #    print(test_data_train_agg.loc[test_data_train_agg['index'] == i, 'gen_WaterDischarge'].item())
            if test_data_train_agg.loc[test_data_train_agg['index'] == i, 'WaterDischarge'].item() < 0:
                test_data_train_agg.loc[test_data_train_agg['index'] == i, 'WaterDischarge'] = 0

        waterFlow_month_test = test_data_train_agg[test_data_train_agg['index'] > index_min]
        waterFlow_month_test['WaterDischarge'] = waterFlow_month_test['WaterDischarge']
        waterFlow_month_test = waterFlow_month_test[['index', 'Year', 'Month', 'WaterDischarge']]
        df = pd.DataFrame(waterFlow_month_test)
        result_file = str(os.path.basename(file_name).split('.')[0])+'_Result.csv'
        df.to_csv(result_file, index=True, header=True)
        # Validation

        # Aggregate the data at month level using Training data
        waterFlow_month_test_agg = waterFlow_month_test.groupby('Month').agg({'WaterDischarge': ['mean', 'std']})
        waterFlow_month_test_agg.columns = waterFlow_month_test_agg.columns.droplevel()
        waterFlow_month_test_agg = waterFlow_month_test_agg.reset_index()
        final = Tk()
        final.minsize(700, 270)
        p_lbl = Label(final, text='Please find the file with Synthetic Data at ', font=('Verdana', 10))
        q_lbl = Label(final, text=str(str(os.getcwd()) + os.sep + result_file), font=('Verdana', 10))
        p_lbl.place(x=40, y=20)
        q_lbl.place(x=40, y=40)

window = Tk()
window.minsize(700, 500)
mywin = MyWindow(window)
window.mainloop()