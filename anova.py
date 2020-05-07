# File to accept data set and return ANOVA table data
"""
Expected Input for the function
    get_anova_linear(<Regression object>, <data set>)
        Regression object format - dictionary {
            "m" : [<array of m values>],
            "dep_var" : [x1, x2, x3.....xn],
            "c": <value of c>
        }
        Data Set format - dictionary {
            "y": <list of y values>,
            "x1" : <list of x1 values>
            "x2" : <list of x2 values>
            "x3" : <list of x3 values> ....
            "xn" : <list of xn values>
        }
Expected Output
    Dictionary object - {
        "ssr": SSR Value,
        "sse": SSE Value,
        "sst": SST Value,
        "msr": MSR Value,
        "mse": MSE Value,
        "s2": s^2 Value,
        "f": F Value
"""


def average(lst):
    return sum(lst) / len(lst)


def calc_y_exp(reg_obj, data_set, index):
    y_exp = 0
    for i in range(len(reg_obj["dep_var"])):
        y_exp += reg_obj["m"][i] * data_set[reg_obj["dep_var"][i]][index]
    y_exp += reg_obj["c"]
    return y_exp


def validate_linear(reg_obj, data_set):
    return True


def get_anova_linear(reg_obj, data_set):
    data_set["y_exp"] = []
    y_mean = average(data_set["y"])
    ssr: int
    ssr = sse = sst = 0
    for i in range(len(data_set["x"])):
        y_exp = calc_y_exp(reg_obj, data_set, i)
        y = data_set["y"][i]
        data_set["y_exp"].append(y_exp)
        ssr = ssr + (y_exp - y_mean) ** 2
        sse = sse + (y_exp - y) ** 2
        sst = sst + (y - y_mean) ** 2
    print(data_set)
    df_r = 1
    df_e = len(data_set["y"]) - 2
    df_t = len(data_set["y"]) - 1
    msr = ssr / df_r
    mse = sse / df_e
    s2 = sst / df_t
    f = msr / mse
    anova_obj = {"ssr": ssr,
                 "sse": sse,
                 "sst": sst,
                 "dfR": df_r,
                 "dfE": df_e,
                 "dfT": df_t,
                 "msr": msr,
                 "mse": mse,
                 "s2": s2,
                 "f": f
                 }
    return anova_obj
