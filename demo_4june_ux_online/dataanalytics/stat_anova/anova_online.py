# File to accept data set and return ANOVA table data
"""
Expected Input for the function
    get_anova_linear(y, ycap, m)
        Data Set format - dictionary {
            "y": <list of y values>,
            "y_exp" : <list of y^ values>,
            "deg_fr" : <degrees of freedom value>
        }
Expected Output
    Dictionary object - {
        "ssr": SSR Value,
        "sse": SSE Value,
        "sst": SST Value,
        "dfR": (m - 1),
        "dfE": (n - m),
        "dfT": (n - 1),
        "msr": MSR Value,
        "mse": MSE Value,
        "s2": s^2 Value,
        "f": F Value
"""


def average(lst):
    return sum(lst) / len(lst)


def get_anova_online(y, ycap, m):
    data_set = {"y": y,"y_exp" : ycap,"deg_fr" : m}
    ssr: int
    ssr = sse = sst = 0
    y_mean = average(data_set["y"])
    for i in range(len(data_set["y"])):
        y = data_set["y"][i]
        y_exp = data_set["y_exp"][i]
        ssr = ssr + (y_exp - y_mean) ** 2
        sse = sse + (y_exp - y) ** 2
        sst = sst + (y - y_mean) ** 2
    m = data_set["deg_fr"]
    n = len(data_set["y"])
    msr = ssr / (m - 1)
    mse = sse / (n - m)
    s2 = sst / (n - 1)
    f = msr / mse
    r2 = ssr/sst
    anova_obj = {"SSR": ssr,
                 "SSE": sse,
                 "SST": sst,
                 "DFR": (m - 1),
                 "DFE": (n - m),
                 "DFT": (n - 1),
                 "MSR": msr,
                 "MSE": mse,
                 "S2": s2,
                 "F": f,
                 "R2":r2,
                 }
    print("## Anova Online Team ##")
    return anova_obj
