import pandas as pd

pandas_data = pd.read_csv("ham_data_reduced.csv")

pandas_data.columns = ["date", 
            "time", 
            "freq", 
            "recieve_strength", 
            "time_offset", 
            "callsigns", 
            "callsign_amount",
            "message",
            "sun_azimuth",
            "sun_elevation" ]

import numpy as np
dat = pandas_data['date'] 
month = np.zeros(np.array(dat).size)
day = np.zeros(np.array(dat).size)
for i in range(np.array(dat).size):
    month[i] = int(str(dat[i])[8:10])
    day[i] = int(str(dat[i])[5:7])

tim = pandas_data['time'] 
hour = np.zeros(np.array(tim).size)
minutes = np.zeros(np.array(tim).size)
seconds = np.zeros(np.array(tim).size)
for i in range(np.array(tim).size): 
  if(len(str(tim[i]))== 6): 
    hour[i] = int(str(tim[i])[0:2]) 
    minutes[i] = int(str(tim[i])[3:5]) 
    seconds[i] = int(str(tim[i])[6:8])

base_freq = np.array(pandas_data["freq"])
rec_str = np.array(pandas_data["recieve_strength"])
time_off = np.array(pandas_data["time_offset"])

callsi_am = pandas_data['callsign_amount']
callsign_am = np.zeros(np.array(callsi_am).size)
for i in range(np.array(callsi_am).size):
    callsign_am[i] = int(int(callsi_am[i])[0:1])

sun_az = np.array(pandas_data["sun_azimuth"])
sun_elev = np.array(pandas_data["sun_elevation"])



from sklearn import preprocessing

x_processed_data = {'hour': hour.astype(int), 'minute': minutes.astype(int), 'seconds': seconds.astype(int),
                  'rs': rec_str, 'to': time_off, 'ca': callsign_am.astype(int), 'sa': sun_az.astype, 'se': sun_elev.astype}

x = pd.DataFrame(x_processed_data)

from sklearn.model_selection import train_test_split 
from sklearn.tree import DecisionTreeClassifier

y = base_freq.astype(str)

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.2)

model = DecisionTreeClassifier()
model.fit(x_train, y_train)

predictions = model.predict(x_test)
from sklearn.metrics import accuracy_score, confusion_matrix, ConfusionMatrixDisplay, classification_report
cm = confusion_matrix(y_test, predictions, labels=model.classes_)
cm

print(classification_report(y_test, predictions, labels=model.classes_))
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=model.classes_)
disp.plot()
accuracy_score(predictions, y_test)
