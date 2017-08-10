# -*- coding: utf-8 -*-
"""
Created on Thu Aug 10 08:15:30 2017

@author: Bana
"""
import pandas as pd
from matplotlib import pyplot as plt
from sklearn.svm import SVR
import numpy as np
from yahoo_finance import Share
import urllib

def calculate(stock):
    s = Share(stock)
    ticker = stock.lower() +".csv"
    try:
        f = pd.read_csv(ticker)
    except:    
        url="https://www.google.com/finance/historical?output=csv&q="+ticker
        stock=ticker+".csv"
        urllib.request.urlretrieve(url,stock)
        f=pd.read_csv(stock)
        
    volumes = list(f['Volume'])
    average = sum(volumes)/len(volumes)
    pertinent = [volumes.index(x) for x  in volumes if x>= average]
    prices = list(f['Close'])
    #ignore the low volume price
    prices_pert = [prices[i] for i in pertinent[::-1]]
    svr_lin = SVR(kernel= 'linear', C= 1e3) 
    X=np.arange(1,len(prices_pert)+1,1.0)
    X=np.reshape(X,(len(X),1))
    y=prices_pert
    y_lin = svr_lin.fit(X, y).predict(X)
    diff = [(y_lin[x]-y[x])/y_lin[x] for x in range(len(y))]
    #support coefficient
    bpd = max(diff)
    #resistance coefficient
    spd = min(diff)
    volatility = bpd-spd
    print("volatiliy: %.3f" %(volatility))
    y_supp = [ i*(1-bpd) for i in y_lin ]
    y_res = [ i*(1+abs(spd)) for i in y_lin ]
    plt.title(s.get_name())
    plt.plot(y_lin)
    plt.plot(prices_pert)
    plt.plot(y_supp,label="Support")
    plt.plot(y_res,label="resistance")
    plt.legend()
    buying_point = diff.index(max(diff))
    gain = y[-1]/y[buying_point]
    return bpd,spf,gain
   
calculate('gs')

       
   




        

