import subprocess
import tkinter as tk
from tkinter import *
from tkinter.filedialog import askopenfile
import os

import pandas as pd


class MyWindow:
    def __init__(self, win):
        self.lbl0 = Label(win, text='Welcome To Time Series Analysis', font=('Verdana', 20))
        self.b1 = Button(win, text='ARIMA_MODELLING', command=lambda: self.run_arima())
        self.b2 = Button(win, text='SYNTHETIC_DATA_GENERATION', command=lambda: self.run_sdg())
        self.b3 = Button(win, text='SMOOTHING_TECHNIQUES', command=lambda: self.run_st())
        self.lbl0.place(x=330, y=15)
        self.b1.place(x=280, y=100)
        self.b2.place(x=420, y=100)
        self.b3.place(x=640, y=100)

    def run_arima(self):
        file_path = str(os.getcwd()) + r"\ARIMA_UI.py"
        cmd = "python " + str(file_path)
        subprocess.call(cmd)

    def run_sdg(self):
        file_path = str(os.getcwd()) + r"\sythetic_data_generation.py"
        cmd = "python " + str(file_path)
        subprocess.call(cmd)

    def run_st(self):
        file_path = str(os.getcwd()) + r"\SmoothingTechniques.py"
        cmd = "python " + str(file_path)
        subprocess.call(cmd)

window = Tk()
window.minsize(1280, 960)
mywin = MyWindow(window)
window.mainloop()

# df = pd.read_csv(r"C:\Users\320074769\Downloads\CCE-IISC\Assignments\Solutions\Assignment 7_Sannihith Reddy\River_Data.csv")
# data_y = df["Monthly Average Data"].values.tolist()
# print(data_y)