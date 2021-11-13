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

'''
#parse time
tim = pandas_data['time'] 
hour = np.zeros(np.array(tim).size)
min = np.zeros(np.array(tim).size)
sec = np.zeros(np.array(tim).size)

print(np.array(tim))

print(tim)

for i in range(np.array(tim).size): #how to specify
    cur_time = str(np.array(tim[i]))

    hour[i] = int(cur_time[0] + cur_time[1]) 
    min[i] = int(cur_time[2] + cur_time[3])#[2:4])
    sec[i] = int(cur_time[4] + cur_time[5])#[4:6])
    
'''
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
#x_time = pandas_data[hour, min, sec][:]
#y1 = pandas_data['freq'][:]
#x4 = pandas_data['rec_send'][:]
x_signal_strength = pandas_data['signal_strgth'].astype(int).to_numpy()
x_device_offset = pandas_data['device_offset_delta_time'].astype(int).to_numpy()
y_base_freq = pandas_data['freq'].astype(str).to_numpy()
#x7 = pandas_data['freq_offset'][:]# n/a
#x_rec_callsign = pandas_data['rec_call_sign'][:]
#x_send_callsign = pandas_data['send_call_sign'][:]
#x_grid_loc = pandas_data['grid_loc'][:]
#x11 = pandas_data['translator'][:]

#https://scikit-learn.org/stable/modules/tree.html#classification ******
from sklearn import tree

print(x_signal_strength.shape)
print(type(x_signal_strength))

X = [
        np.concatenate((x_signal_strength, x_device_offset), axis = 1) #, x_rec_callsign, x_send_callsign, x_grid_loc
    #'''
    #[0, 0], #[dat,tim,.........]
    #[1, 1]
    #'''
    #..... #features = all other variables 0 = (number of samples , number of features ) * every row is sample* 
    ]

#print(X)
#print(type(X))

from sklearn.preprocessing import LabelBinarizer
#y = np.array(["7.074", "10.136", "14.074", "18.100", "21.074", "28.074"]) #target = freq
#print(y)
y_dense = LabelBinarizer().fit_transform(y_base_freq)
print(y_dense)

print("worked")

'''
from scipy import sparse
y_sparse = sparse.csr_matrix(y_dense)
print(y_sparse)
'''

clf = tree.DecisionTreeClassifier()
clf = clf.fit(X, y_dense)

clf.predict([[2., 2.]])
#array([1])

from sklearn.datasets import load_iris #ham_dataV2.csv????
from sklearn import tree
iris = load_iris()
X, y = iris.data, iris.target
clf = tree.DecisionTreeClassifier()
clf = clf.fit(X, y_dense)
