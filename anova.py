# File to accept data set and return ANOVA table data
"""
Expected Input for the function
    get_anova_linear(<Regression object>, <data set>)
        Regression object format - dictionary {"m" : <value of m>, "c: <value of c>}
        Data Set format - dictionary { "y": <list of y values>, "x" : <list of x values>}
Expected Output
    Dictionary object - {
        ssr: SSR Value,
        "sse": SSE Value,
         "sst": SST Value,
         "msr": MSR Value,
         "mse": MSE Value,
         "s2": s^2 Value,
         "f": F Value
"""


def average(lst):
    return sum(lst) / len(lst)


def get_anova_linear(reg_obj, data_set):
    data_set["y_exp"] = []
    y_mean = average(data_set["y"])
    ssr = sse = sst = 0
    m = reg_obj["m"]
    c = reg_obj["c"]
    for i in range(len(data_set["x"])):
        y_exp = m * data_set["x"][i] + c
        y = data_set["y"][i]
        data_set["y_exp"].append(y_exp)
        ssr = ssr + (y_exp - y_mean)**2
        sse = sse + (y_exp - y)**2
        sst = sst + (y - y_mean)**2
    print(data_set)
    msr = ssr;
    mse = sse/(len(data_set["x"]) - 2)
    s2 = sst/(len(data_set["x"]) - 1)
    f = msr/mse
    anova_obj = {"ssr": ssr,
                 "sse": sse,
                 "sst": sst,
                 "msr": msr,
                 "mse": mse,
                 "s2": s2,
                 "f": f}
    return anova_obj
