from tkinter import *
from tkinter.filedialog import askopenfile
import tkinter as tk
import matplotlib.pyplot as plt
import pandas as pd
from math import sqrt
import statsmodels.tsa.stattools
from pandas import DataFrame

import udf
from linear_regression import LinearRegression


class MyWindow:
    flag = 0
    flag_nor = 0
    flag_sea = 0

    def __init__(self, win):
        self.lbl0 = Label(win, text='Welcome To ARIMA Model')
        self.lbl1 = Label(win, text='Input Excel file path')
        self.lbl2 = Label(win, text='Index')
        self.lbl3 = Label(win, text='Column Name')
        self.lbl4 = Label(win, text='Number of lags')
        self.entry_text = tk.StringVar()
        self.t1 = Entry(window, textvariable=self.entry_text)
        self.t2 = Entry()
        self.t3 = Entry()
        self.t4 = Entry()
        self.b1 = Button(win, text='Browse', command=lambda: self.open_file())
        self.b2 = Button(win, text='Submit', command=lambda: self.get_data())
        self.lbl0.place(x=150, y=15)
        self.lbl1.place(x=90, y=50)
        self.lbl2.place(x=90, y=100)
        self.lbl3.place(x=90, y=150)
        self.lbl4.place(x=90, y=200)
        self.t1.place(x=200, y=50)
        self.t2.place(x=200, y=100)
        self.t3.place(x=200, y=150)
        self.t4.place(x=200, y=200)
        self.b1.place(x=332, y=50)
        self.b2.place(x=200, y=250)

    def get_data(self):
        self.file_path = str(self.t1.get())
        self.sheet_name = str(self.t2.get())
        self.column_index = str(self.t3.get())
        self.lag_count = int(self.t4.get())
        df = pd.read_excel(str(self.t1.get()), sheet_name=str(self.t2.get()))
        data_y = df[str(self.t3.get())].values.tolist()
        return self.plot_input_data(data_y, int(self.t4.get()))

    def open_file(self):
        file = askopenfile(mode='r', filetypes=[('Excel Files', '*.xls')])
        self.entry_text.set(file.name)

    def get_x_axis_values(self, val):
        x = []
        temp = 0
        for x_axis in range(val):
            temp = temp + 1
            x.append(temp)
        return x

    def ACF(self, Y, lags):
        ACF_list = []
        r = []
        for i in range(lags):
            data_y = Y
            data_y = [x for x in data_y if str(x) != 'nan']
            data_lag = Y
            data_lag = [x for x in data_lag if str(x) != 'nan']
            for j in range(i + 1):
                data_y.pop(0)
                data_lag.pop(len(data_lag) - 1)
            r.append(1.96 / sqrt(len(data_lag)))
            Ysum = 0
            Lsum = 0
            for i in range(len(data_y)):
                Ysum = Ysum + data_y[i]
            Ybar = Ysum / len(data_y)
            for i in range(len(data_lag)):
                Lsum = Lsum + data_lag[i]
            Lbar = Lsum / len(data_lag)
            Y_Ybar = []
            for i in range(len(data_y)):
                Y_Ybar.append(data_y[i] - Ybar)
            L_Lbar = []
            for i in range(len(data_lag)):
                L_Lbar.append(data_lag[i] - Lbar)
            product = []
            for i in range(len(data_lag)):
                product.append(Y_Ybar[i] * L_Lbar[i])
            sum_product = 0
            for i in range(len(data_lag)):
                sum_product = sum_product + product[i]
            numerator = sum_product
            sq_Y_Ybar = []
            for i in range(len(data_y)):
                sq_Y_Ybar.append(Y_Ybar[i] * Y_Ybar[i])
            sum_sq_Y_Ybar = 0
            for i in range(len(data_lag)):
                sum_sq_Y_Ybar = sum_sq_Y_Ybar + sq_Y_Ybar[i]
            sq_L_Lbar = []
            for i in range(len(data_y)):
                sq_L_Lbar.append(L_Lbar[i] * L_Lbar[i])
            sum_sq_L_Lbar = 0
            for i in range(len(data_lag)):
                sum_sq_L_Lbar = sum_sq_L_Lbar + sq_L_Lbar[i]
            product_squ = sum_sq_Y_Ybar * sum_sq_L_Lbar
            denominator = sqrt(product_squ)
            result = numerator / denominator
            ACF_list.append(result)
            self.ACF_Data = ACF_list
            self.r__ACF_Data = r
        return ACF_list

    def PACF(self, Y, lags):
        PACF = statsmodels.tsa.stattools.pacf_yw(Y, nlags=lags, method='unbiased')
        PACF_list = PACF.tolist()
        PACF_list.pop(0)
        self.PACF_Data = PACF_list
        self.r_PACF_Data = 1.96 / sqrt(len(Y) - lags)
        return PACF_list

    def plot_input_data(self, data_y, lag_count):
        self.refined_Data = data_y
        data_y = [x for x in data_y if str(x) != 'nan']
        lag_count_val = lag_count
        plt.close('all')
        y = data_y
        x = self.get_x_axis_values(len(data_y))
        plt.plot(x, y)
        plt.title('Input Data')
        wm = plt.get_current_fig_manager()
        wm.window.wm_geometry("600x500+0+0")
        fig = plt.figure()
        ax2 = fig.add_subplot(3, 1, 1)
        y_acf = self.ACF(data_y, lag_count_val)
        x_acf = self.get_x_axis_values(len(y_acf))
        ax2.bar(x_acf, y_acf, color='red')
        plt.axhline(0, color='black')
        plt.axvline(0, color='black')
        plt.title('ACF Plot')
        r = []
        for sign in range(len(x_acf)):
            r.append(1.96 / sqrt(len(data_y)))
        plt.plot(x_acf, r, color='green')
        ax3 = fig.add_subplot(3, 1, 3)
        y_pacf = self.PACF(data_y, lag_count_val)
        x_pacf = self.get_x_axis_values(len(y_pacf))
        ax3.bar(x_pacf, y_pacf, color='red')
        plt.axhline(0, color='black')
        plt.axvline(0, color='black')
        plt.title('PACF Plot')
        wm = plt.get_current_fig_manager()
        wm.window.wm_geometry("600x500+630+0")
        window.quit()
        return self.get_stationarity_status(data_y)

    def get_stationarity_status(self, data_y):
        root = Tk()
        root.minsize(300, 200)
        root.geometry("500x100+400+500")
        lbl4 = Label(root, text='Is Data Stationary?', font=('Verdana', 20))
        btn_yes = Button(root, text='YES', command=lambda: self.get_p_q(root))
        btn_no = Button(root, text='NO', command=lambda: self.get_differencing_status(root, data_y))
        lbl4.place(x=100, y=20)
        btn_yes.place(x=100, y=70)
        btn_no.place(x=150, y=70)
        plt.show()

    def warn_message(self, warn):
        warn.destroy()
        self.get_p_q("none")

    def get_differencing_status(self, root, data_y):
        root.destroy()
        diff = Tk()
        self.flag = self.flag + 1
        diff.minsize(300, 200)
        diff.geometry("500x100+400+500")
        diff_lbl = Label(diff, text='Proceed With...', font=('Verdana', 20))
        diff_lbl.place(x=100, y=100)
        btn_seas = Button(diff, text='Seasonal Differencing', command=lambda: self.get_seasonal_freq(diff, data_y))
        btn_normal = Button(diff, text='Normal Differencing', command=lambda: self.do_normal_differencing(diff, data_y))
        btn_seas.place(x=100, y=70)
        btn_normal.place(x=250, y=70)
        if self.flag == 0:
            diff.destroy()

    def get_seasonal_freq(self, diff, data_y):
        diff.destroy()
        self.flag_sea = self.flag_sea + 1
        if self.flag_sea == 3:
            self.flag = 0
            self.flag_nor = 0
            self.flag_sea = 0
            warn = Tk()
            warn.minsize(300, 200)
            warn.geometry("500x100+400+500")
            warn_lbl = Label(warn, text='Max Differencing Limit Reached', font=('Verdana', 20))
            warn_lbl.place(x=100, y=70)
            btn_warn = Button(warn, text='Ok', command=lambda: self.warn_message(warn))
            btn_warn.place(x=100, y=100)
        if self.flag != 0:
            seasonal = Tk()
            seasonal.minsize(300, 200)
            seasonal.geometry("500x100+400+500")
            seasonal_lbl = Label(seasonal, text='Enter Seasonal Frequency', font=('Verdana', 20))
            seasonal_lbl.place(x=100, y=20)
            self.freq = Entry(seasonal)
            self.freq.place(x=100, y=70)
            btn_submit = Button(seasonal, text='Submit',
                                command=lambda: self.do_seasonal_differencing(seasonal, data_y, self.freq.get()))
            btn_submit.place(x=100, y=120)

    def do_seasonal_differencing(self, seasonal, Y, freq):
        seasonal.destroy()
        seasonality_freq = int(freq)
        temp_data = []
        for i in range(len(Y) - seasonality_freq):
            temp_data.append(Y[i + seasonality_freq])
        temp_data = [x for x in temp_data if str(x) != 'nan']
        data_seaso_diff = []
        for i in range(len(temp_data)):
            data_seaso_diff.append(temp_data[i] - Y[i])
        return self.plot_input_data(data_seaso_diff, self.lag_count)

    def do_normal_differencing(self, diff, Y):
        self.flag_nor = self.flag_nor + 1
        if self.flag_nor == 3:
            self.flag = 0
            self.flag_nor = 0
            self.flag_sea = 0
            warn = Tk()
            warn.minsize(300, 200)
            warn.geometry("500x100+400+500")
            warn_lbl = Label(warn, text='Max Differencing Limit Reached', font=('Verdana', 10))
            warn_lbl.place(x=100, y=70)
            btn_warn = Button(warn, text='Ok', command=lambda: self.warn_message(warn))
            btn_warn.place(x=100, y=100)
        diff.destroy()
        temp_data = []
        for i in range(len(Y) - 1):
            temp_data.append(Y[i + 1])
        temp_data = [x for x in temp_data if str(x) != 'nan']
        data_normal_diff = []
        for i in range(len(temp_data)):
            data_normal_diff.append(temp_data[i] - Y[i])
        if self.flag != 0:
            return self.plot_input_data(data_normal_diff, self.lag_count)

    def get_p_q(self, root):
        if root != "none":
            root.destroy()
        ACF_Val = self.ACF_Data
        r_ACF = self.r__ACF_Data
        PACF_Val = self.PACF_Data
        r_PACF = self.r_PACF_Data
        p_list = []
        for i in range(25):
            if PACF_Val[i] > r_PACF or PACF_Val[i] < -r_PACF:
                p_list.append(i)
        p_list.sort()
        p_list.reverse()
        p = p_list[0] + 1
        q_list = []
        for i in range(25):
            if ACF_Val[i] > r_ACF[i] or ACF_Val[i] < -r_ACF[i]:
                q_list.append(i)
        q_list.sort()
        q_list.reverse()
        q = q_list[0] + 1
        final = Tk()
        final.minsize(600, 270)
        p_lbl = Label(final, text='Suggested p Value is ' + str(p), font=('Verdana', 10))
        q_lbl = Label(final, text='Suggested q Value is ' + str(q), font=('Verdana', 10))
        p_val = Label(final, text='Set p Value to ', font=('Verdana', 10))
        q_val = Label(final, text='Set q Value to ', font=('Verdana', 10))
        p_val_user = Entry(final)
        q_val_user = Entry(final)
        p_lbl.place(x=100, y=20)
        p_val.place(x=100, y=70)
        p_val_user.place(x=200, y=70)
        q_lbl.place(x=100, y=120)
        q_val.place(x=100, y=170)
        q_val_user.place(x=200, y=170)
        btn_submit = Button(final, text='Submit', command=lambda: self.cal_coeff(final, p_val_user.get(), q_val_user.get()))
        btn_submit.place(x=100, y=220)
        # window.destroy()

    def cal_coeff(self, final, p, q):
        data_z = self.refined_Data
        final.destroy()
        plt.close('all')
        p = int(p)
        q = int(q)
        if q == 0:
            df = pd.read_excel(str(self.t1.get()), sheet_name=str(self.t2.get()))
            data_y = df[str(self.t3.get())]
            ip_ts = data_y.dropna().to_numpy()
            y_var = ip_ts[p:].tolist()
            x_var = []
            Yt = ""
            for i in range(1, p+1):
                tmp = udf.shift(ip_ts, i)
                tmp_lst = tmp[p:].tolist()
                x_var.append(tmp_lst)
            tmp_obj = LinearRegression()
            reg_out = tmp_obj.fit(x_var, y_var)
            reg_coeff = reg_out[1]
            for j in range(1, p+1):
                Yt = Yt + "(" + str(round(reg_coeff[j-1], 3)) + ")" + "*Yt-" + str(j) + " + "
            Yt = "Yt = " + str(Yt[:-2])
            reg = Tk()
            reg.minsize(800, 150)
            p_lbl = Label(reg, text='AR Equation is...', font=('Verdana', 10))
            q_lbl = Label(reg, text=Yt, font=('Verdana', 10))
            p_lbl.place(x=100, y=20)
            q_lbl.place(x=100, y=70)
        if p == 0:
            data_y = data_z
            data_y = [x for x in data_y if str(x) != 'nan']
            temp = []
            for i in range(len(data_y)):
                temp.append(data_y[i] - sum(data_y) / len(data_y))
            sum_temp = 0
            for j in range(len(temp)):
                sum_temp = sum_temp + (temp[j] - sum(temp) / len(temp)) * (temp[j] - sum(temp) / len(temp))
            white_noise_var = sum_temp / (len(temp) - 1)
            covariance = []
            data_y_temp = data_y
            data_lag = data_y
            for j in range(q + 1):
                data_y_temp.pop(0)
                data_lag.pop(len(data_lag) - 1)
                z = []
                for x in range(len(data_y_temp)):
                    z.append((data_y_temp[x] - (sum(data_y_temp) / len(data_y_temp))) * (
                            data_lag[x] - (sum(data_lag) / len(data_lag))))
                covariance.append(sum(z) / (len(data_y_temp) - 1))
            teta_list = []
            Yt = ""
            if q == 1:
                teta_1 = (covariance[0]) / (white_noise_var)
                Yt = 'yt = ' + str(1) + ' + ' + str(round(teta_1, 3)) + '*' + 'epsion_t-1'
                teta_list.append(teta_1)
            elif q == 2:
                teta_2 = (covariance[1]) / (white_noise_var)
                teta_1 = (covariance[0]) / ((white_noise_var) * (1 + teta_2))
                Yt = 'Yt = ' + str(1) + ' + ' + str(round(teta_1, 3)) + '*' + 'epsilon_t-1' + ' + ' + str(round(teta_2, 3)) \
                     + '*' + 'epsilon_t-2'
                teta_list.append(teta_1)
                teta_list.append(teta_2)
            reg = Tk()
            reg.minsize(800, 150)
            p_lbl = Label(reg, text='MA Equation is...', font=('Verdana', 10))
            q_lbl = Label(reg, text=Yt, font=('Verdana', 10))
            p_lbl.place(x=100, y=20)
            q_lbl.place(x=100, y=70)


window = Tk()
window.minsize(1280, 960)
mywin = MyWindow(window)
window.title('ARIMA MODEL')

window.mainloop()
