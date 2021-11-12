# -*- coding: utf-8 -*-
"""
Created on Fri Oct 15 14:44:27 2021

@author: brian
"""


import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

pandas_data = pd.read_csv("no_payload_ham_data.csv", sep = ",", names=['date', 'time', 
                                                            'freq', 'signal_strgth',
                                                            'device_offset_delta_time',
                                                            'freq_offset'])
                                                            #'''
                                                            #'rec_call_sign',
                                                            #'send_call_sign', 'grid_loc' ])
                                                            #'''

# clean data: 
# freq (number format)  *****
# make values discrete 
# look for non discrete & convert ***


#'''
#parse date 
#dat = pandas_data['date'] 
#year = np.zeros(np.array(dat).size)
#month = np.zeros(np.array(dat).size)
#day = np.zeros(np.array(dat).size)
#for i in range(np.array(dat).size):
#    year[i] = int(str(dat[i])[0:2]) 
#    month[i] = int(str(dat[i])[2:4])
#    day[i] = int(str(dat[i])[4:6])
#'''

#parse time
tim = pandas_data['time'] 
hour = np.zeros(np.array(tim).size)
min = np.zeros(np.array(tim).size)
sec = np.zeros(np.array(tim).size)

print(hour)
print(min)
print(sec)

print(np.array(tim))


for i in range(np.array(tim).size):  
    print(i)
    hour[i] = int((tim[i])[0:2]) 
    min[i] = int((tim[i])[2:4])
    sec[i] = int((tim[i])[4:6])
    
#'''
##parse rec call sign 
#rloc = pandas_data['rec_call_sign'] 
#char2 = np.zeros(np.array(rloc).size)
#for i in range(np.array(rloc).size):
#    char2[i] = int(str(rloc[i])[0:2]) 
#'''


# x = pandas_data['time'][:]
# y = pandas_data['signal_strgth'][:]
# z = pandas_data['grid_loc'][:]

# plt.figure()


# plt.plot(x,y, '.', color='black')

# plt.show()

#x1 = pandas_data['date'][:]
x_time = pandas_data[hour, min, sec][:]
#y1 = pandas_data['freq'][:]
#x4 = pandas_data['rec_send'][:]
x_signal_strength = pandas_data['signal_strgth'][:]
x_device_offset = pandas_data['device_offset_delta_time'][:]
#x7 = pandas_data['freq_offset'][:]# n/a
#x_rec_callsign = pandas_data['rec_call_sign'][:]
#x_send_callsign = pandas_data['send_call_sign'][:]
#x_grid_loc = pandas_data['grid_loc'][:]
#x11 = pandas_data['translator'][:]

#https://scikit-learn.org/stable/modules/tree.html#classification ******
from sklearn import tree
X = [
        x_time, x_signal_strength, x_device_offset #, x_rec_callsign, x_send_callsign, x_grid_loc
    #'''
    #[0, 0], #[dat,tim,.........]
    #[1, 1]
    #'''
    #..... #features = all other variables 0 = (number of samples , number of features ) * every row is sample* 
    ]

from sklearn.preprocessing import LabelBinarizer
Y = [7.074, 10.136, 14.074, 18.100, 21.074, 28.074] #target = freq
Y = LabelBinarizer().fit_transorm(Y)
clf = tree.DecisionTreeClassifier()
clf = clf.fit(X, Y)

clf.predict([[2., 2.]])
#array([1])

from sklearn.datasets import load_iris #ham_dataV2.csv????
from sklearn import tree
iris = load_iris()
X, y = iris.data, iris.target
clf = tree.DecisionTreeClassifier()
clf = clf.fit(X, y)
