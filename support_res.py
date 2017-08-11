# -*- coding: utf-8 -*-
"""
Created on Thu Aug 10 08:15:30 2017

@author: Bana
"""
import pandas as pd
from matplotlib import pyplot as plt
import matplotlib.dates as dates
from sklearn.svm import SVR
import numpy as np
from yahoo_finance import Share
import urllib



def calculate(stock,data=None):
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
    
    if data==None or data==1:
        pertinent = [volumes.index(x) for x  in volumes if x>= average]
    else:
        pertinent = [volumes.index(x) for x  in volumes if x>= average][:data]
    
    
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
    plt.plot(y)
    plt.plot(y_supp,label="Support")
    plt.plot(y_res,label="resistance")
    plt.legend()
    plt.show()
    buying_point = diff.index(max(diff))
    gain = y[-1]/y[buying_point]
    return len(pertinent)

def main():   
    ulang = 1 
    while (ulang!=None):
        data = calculate('ko',ulang)
        ulang = int(eval(input("Input Data Length (Max:%d): " %(data))))
        
if __name__=="__main__":
    main()        
