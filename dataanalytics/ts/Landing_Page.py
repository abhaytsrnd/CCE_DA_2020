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
        cmd = "python3 " + self.path('ARIMA_UI.py')
        os.system(cmd)

    def run_sdg(self):
        cmd = "python3 " + self.path('sythetic_data_generation.py')
        os.system(cmd)

    def run_st(self):
        cmd = "python3 " + self.path('SmoothingTechniques.py')
        os.system(cmd)

    def path(self, file: str):
        print('### Path : '+ file)
        os.system('pwd')
        #path = os.path.join(str(os.getcwd()), 'dataanalytics')
        path = os.path.join('dataanalytics', 'ts')
        path = os.path.join(path, file)
        print('### Path : '+ path)
        return str(path)

window = Tk()
window.minsize(1280, 960)
mywin = MyWindow(window)
window.mainloop()
