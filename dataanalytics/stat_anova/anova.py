# -*- coding: utf-8 -*-
"""
Created on Fri May  8 09:20:42 2020

@author: Madhurya, yashaswi, team
"""
def get_anova(y, ycap, m):
    import scipy.stats
    n = len(y)
    #obtain ybar
    sumy = 0
    for i in y:
        sumy = sumy+i
    ybar = sumy/(len(y))

    #Obtain sigma((ycap-ybar)^2) -- SSR
    yd = []
    yds = []
    for i in ycap:
        yd.append(i-ybar)
    for i in yd:
        yds.append(i**2)
    SSR = 0
    for i in yds:
        SSR = SSR+i
    #print('SSR:', SSR)

    #Obtain sigma((ycap-y)^2) -- SSE
    ye = []
    yes = []
    SSE = 0
    j = 0
    for i in y:
        ye.append(i-ycap[j])
        j = j+1
    for i in ye:
        yes.append(i**2)
    #print(yes)
    for i in yes:
        SSE =  SSE+i
    #print('SSE:', SSE)

    #Obtain sigma((y-ybar)^2) -- SST
    yd = []
    yds = []
    for i in y:
        yd.append(i-ybar)
    for i in yd:
        yds.append(i**2)
    SST = 0
    for i in yds:
        SST = SST+i
    #print('SST:', SST)

    MSR = SSR/(m-1)
    MSE = SSE/(n-m)
    F = MSR/MSE
    f_critical = scipy.stats.f.ppf(q=0.025, dfn=m-1, dfd=n-m)
    S_sq = SST/(n-1)

    rsq=SSR/SST
    adj_rsq=1-((1-rsq)*(n-1)/(n-m-1))

    #print("The value of MSE is", MSE)
    #print("The value of MSR is", MSR)
    #print("The value of F is", F)
    #print("The value of F-Critical is", f_critical)
    #print("The value of S_sq is", S_sq)
    #print("The value of R-square is", rsq)
    #print("The value of ADJ-R-square is", adj_rsq)

    #anova_op = {'SSR': SSR, 'SSE':SSE, 'SST':SST, 'MSR':MSR, 'MSE':MSE, 'F':F, 'f_critical':f_critical, 'S_sq':S_sq, 'rsq':rsq, 'adj_rsq':adj_rsq}
    anova_op = {'SSR': SSR, 'SSE':SSE, 'SST':SST, "DFR": (m - 1), "DFE": (n - m), "DFT": (n - 1), 'MSR':MSR, 'MSE':MSE, 'F':F, 'S2':S_sq, 'R2':rsq}
    print("## Anova Class Team ##")
    return anova_op
