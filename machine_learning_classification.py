# -*- coding: utf-8 -*-
"""
Created on Fri Oct 15 14:44:27 2021

@author: brian
"""


import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

pandas_data = pd.read_csv("ham_dataV2.csv", sep = ",", names=['date', 'time', 
                                                            'freq','rec_send', 
                                                            'translator', 'signal_strgth',
                                                            'device_offset_delta_time',
                                                            'freq_offset', 'rec_call_sign',
                                                            'send_call_sign', 'grid_loc' ])

# clean data: 
# freq (number format)  *****
# make values discrete 
# look for non discrete & convert ***



#parse date 
dat = pandas_data['date'] 
year = np.zeros(np.array(dat).size)
month = np.zeros(np.array(dat).size)
day = np.zeros(np.array(dat).size)
for i in range(np.array(dat).size):
    year[i] = int(str(dat[i])[0:2]) 
    month[i] = int(str(dat[i])[2:4])
    day[i] = int(str(dat[i])[4:6])


# x = pandas_data['time'][:]
# y = pandas_data['signal_strgth'][:]
# z = pandas_data['grid_loc'][:]

# plt.figure()


# plt.plot(x,y, '.', color='black')

# plt.show()

x1 = pandas_data['date'][:]

xz = pandas_data['day'][:]

x2 = pandas_data['time'][:]
y1 = pandas_data['freq'][:]
x4 = pandas_data['rec_send'][:]
x5 = pandas_data['signal_strgth'][:]
x6 = pandas_data['device_offset_delta_time'][:]
x7 = pandas_data['freq_offset'][:]# n/a
x8 = pandas_data['rec_call_sign'][:]
x9 = pandas_data['send_call_sign'][:]
x10 = pandas_data['grid_loc'][:]
x11 = pandas_data['translator'][:]


 from sklearn import tree
 X = [
      [0, 0],
      [1, 1]
     #..... #features = all other variables 0 = (number of samples , number of features ) * every row is sample* 
     
     ]
 Y = [0, 1] #target = freq
 clf = tree.DecisionTreeClassifier()
 clf = clf.fit(X, Y)
    
 clf.predict([[2., 2.]])
 array([1])
    
 from sklearn.datasets import load_iris #ham_dataV2.csv????
 from sklearn import tree
 iris = load_iris()
 X, y = iris.data, iris.target
 clf = tree.DecisionTreeClassifier()
 clf = clf.fit(X, y)
