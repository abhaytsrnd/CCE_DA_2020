import os

import pandas as pd
import matplotlib.pyplot as plt
from tkinter.filedialog import askopenfile
from tkinter import *
import tkinter as tk


class MyWindow:
    def __init__(self, win):
        self.lbl0 = Label(win, text='Welcome To Smoothing Techniques', font=('Verdana', 20))
        self.lbl1 = Label(win, text='Input CSV file path')
        self.entry_text = tk.StringVar()
        self.t1 = Entry(window, textvariable=self.entry_text)
        self.b1 = Button(win, text='Browse', command=lambda: self.open_file())
        self.b2 = Button(win, text='Submit', command=lambda: self.get_data())
        self.lbl0.place(x=100, y=15)
        self.lbl1.place(x=90, y=100)
        self.t1.place(x=200, y=100)
        self.b1.place(x=332, y=100)
        self.b2.place(x=200, y=150)

    def get_data(self):
        self.file_path = str(self.t1.get())
        data = pd.read_csv(self.file_path)
        df = pd.DataFrame()
        df = data.copy()
        return self.smoothing_type(df)

    def open_file(self):
        file = askopenfile(mode='r', filetypes=[('CSV Files', '*.csv')])
        self.entry_text.set(file.name)

    def smoothing_type(self, df):
        diff = Tk()
        diff.minsize(300, 200)
        diff.geometry("500x100+400+500")
        diff_lbl = Label(diff, text='Proceed With...', font=('Verdana', 10))
        diff_lbl.place(x=100, y=70)
        btn_seas = Button(diff, text='Exponential Smoothing', command=lambda: self.smoothing_factor(df))
        btn_normal = Button(diff, text='Moving Average Smoothing', command=lambda: self.moving_avg(df))
        btn_seas.place(x=100, y=100)
        btn_normal.place(x=250, y=100)

    def smoothing_factor(self, df):
        master = Tk()
        master.minsize(300, 200)
        variable = StringVar(master)
        variable.set("0.6")  # default value
        labl = Label(master, text='Select Smoothing Factor', font=('Verdana', 10))
        opt = OptionMenu(master, variable, "0.5", "0.6", "0.7")
        btn_normal = Button(master, text='Ok', command=lambda: self.exponential(df, variable.get()))
        labl.place(x=100, y=70)
        opt.place(x=100, y=120)
        btn_normal.place(x=100, y=170)
        print(variable.get())
        return

    def moving_avg(self, df):
        master = Tk()
        master.minsize(300, 200)
        variable = StringVar(master)
        variable.set("3")  # default value
        labl = Label(master, text='Select Moving Average', font=('Verdana', 10))
        opt = OptionMenu(master, variable, "3", "5", "7")
        btn_normal = Button(master, text='Ok', command=lambda: self.movingAverage(df, variable.get()))
        labl.place(x=100, y=70)
        opt.place(x=100, y=120)
        btn_normal.place(x=100, y=170)
        print(variable.get())
        return

    def exponential(self, df, val):
        plt.close('all')
        i = 0
        forecast_list = []
        sf = float(val)
        cols = list(df.columns)
        new_frame = pd.DataFrame()
        for cl in cols:
            new_list = df[cl].tolist()
            if i == 0:
                new_frame.insert(i, cl, new_list)
                i += 1
            else:
                new_frame.insert(i, 'Actual Sales', new_list)
                for k in range(len(new_list)):
                    if k == 0:
                        temp_forecast_value = new_list[k]
                    else:
                        temp_forecast_value = round((sf * new_list[k]) + ((1 - sf) * forecast_list[k - 1]), 2)
                    forecast_list.insert(k, temp_forecast_value)
                new_frame.insert(i, "Exponential " + cl + "(" + str(sf) + ")", forecast_list)
                result_file = str(os.path.basename(self.file_path).split('.')[0]) + '_Exp_Result.csv'
                new_frame.to_csv(result_file, index=True, header=True)
                plt.plot(new_frame['Time period'], new_frame["Exponential " + cl + "(" + str(sf) + ")"],
                         linestyle='solid')
                plt.plot(new_frame['Time period'], new_frame['Actual ' + cl], linestyle='dashed')
                plt.legend()
                plt.show()

    def movingAverage(self, df, val):
        plt.close('all')
        i = 0
        m = 0
        ma_list = []
        ma = int(val)
        cols = list(df.columns)
        new_frame = pd.DataFrame()
        for cl in cols:
            new_list = df[cl].tolist()
            if i == 0:
                new_frame.insert(i, cl, new_list)
                i += 1
            else:
                new_frame.insert(i, cl, new_list)
                for k in range(len(new_list)):
                    if k < (int((ma) / 2)):
                        temp_ma_value = None
                    elif m + ma <= len(new_list) and new_list[m:m + ma] != new_list[m - 1:m + ma - 1]:
                        temp_ma_value = round(sum(new_list[m:m + ma]) / len(new_list[m:m + ma]), 2)
                        m += 1
                    ma_list.insert(k, temp_ma_value)
                    temp_ma_value = None
                new_frame.insert(i, str(ma) + ' Monthly Moving Average ' + cl, ma_list)
                result_file = str(os.path.basename(self.file_path).split('.')[0]) + '_MA_Result.csv'
                new_frame.to_csv(result_file, index=True, header=True)
                plt.plot(new_frame['Time period'], new_frame[str(ma) + ' Monthly Moving Average ' + cl],
                         linestyle='solid')
                plt.plot(new_frame['Time period'], new_frame[cl], linestyle='dashed')
                plt.legend()
                plt.show()


window = Tk()
window.minsize(700, 500)
mywin = MyWindow(window)
window.mainloop()

