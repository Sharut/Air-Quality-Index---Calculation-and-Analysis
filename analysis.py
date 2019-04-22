#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 20 00:16:50 2019

@author: uiet_mac1
"""

import csv
import numpy as np

row_count=0
with open("data1.csv", 'r') as f:
    for line in f:
        row_count += 1
row_count = row_count - 1
first_row = True
X = np.zeros((row_count, 6))
with open("data1.csv", 'r') as train_file:
    csv_reader = csv.reader(train_file, delimiter=',')
    i = 0
    for row in csv_reader:
        if first_row:
            first_row = False
            continue
        row = [w.replace('None', 'nan') for w in row]
        X[i] = row[2:]
        i=i+1

PM25 = X[:, 0]
PM10 = X[:, 1]
SO2 = X[:, 2]
NO2 = X[:, 3]
O3 = X[:, 4]
CO = X[:, 5]

#Eight hour average defined
def EightHrAvg(X):
    Y = np.zeros((int(np.size(X, 0)/8), 1))
    for i in range(0, np.size(X, 0), 8):
        Y[int(i/8)] = np.nanmean(X[i:i+8])
    return Y

#Twenty four hour average defined
def TwentyFourHrAvg(X):
    flag=1
    Y = np.zeros((int(np.size(X, 0)/24), 1))
    for i in range(0, np.size(X, 0), 24):
        if (int(i/24)==474 and flag==1):
            Y[int(i/24)] = np.nanmean(X[i:i+1])
            flag=0
        elif (flag==1):
            Y[int(i/24)] = np.nanmean(X[i:i+24])
    return Y

#How to calculate AQI
def AQI(X, vals):
    aqi = [50, 100, 200, 300, 400]
    aqi_vals = np.zeros((np.size(X, 0)))

    for i in range(np.size(X, 0)):
        prev_val = 0
        prev_aqi = 0
        for j in range(np.size(vals, 0)):
            if X[i] <= vals[j]:
                aqi_vals[i] = prev_aqi + (X[i] - prev_val) / (vals[j] - prev_val) * (aqi[j]-prev_aqi)
                break
            prev_aqi = aqi[j]-1
            prev_val = vals[j]
    return aqi_vals


#calculate 24-hour average for PM25, PM10, SO2, NO2
PM25_avg = TwentyFourHrAvg(PM25)
PM10_avg = TwentyFourHrAvg(PM10)
SO2_avg = TwentyFourHrAvg(SO2)
NO2_avg = TwentyFourHrAvg(NO2)

#calculate 8-hour average for O3, CO
O3_avg = EightHrAvg(O3)
CO_avg = EightHrAvg(CO)

#calculate the AQI sub-indices
AQI_PM25 = AQI(PM25_avg, [30, 60, 90, 120, 250])
AQI_PM10 = AQI(PM10_avg, [50, 100, 250, 350, 430])
AQI_SO2 = AQI(SO2_avg, [40, 80, 380, 800, 1600])
AQI_NO2 = AQI(NO2_avg, [40, 80, 180, 280, 400])
AQI_O3_temp = AQI(O3_avg, [50, 100, 168, 208, 748])
AQI_CO_temp = AQI(CO_avg, [1, 2, 10, 17, 34])

AQI_O3 = np.zeros((int(np.size(AQI_O3_temp, 0)/3)))
AQI_CO = np.zeros((int(np.size(AQI_CO_temp, 0)/3)))

#find the max out of the 8 hour averages for O3 and CO
for i in range(0, np.size(AQI_O3, 0), 3):
    AQI_O3[int(i/3)] = np.max(AQI_O3_temp[i:i+2])
    AQI_CO[int(i/3)] = np.max(AQI_CO_temp[i:i+2])


#calculate the AQI for each day
AQI = np.zeros((np.size(AQI_PM10, 0)))
for i in range(np.size(AQI_PM10, 0)):
    AQI[i] = np.max([AQI_PM25[i], AQI_PM10[i], AQI_SO2[i], AQI_NO2[i], AQI_O3[i], AQI_CO[i]])

with open('my_data.csv', 'a') as csvFile:
        row = ['PM2.5','PM10','SO2','NO2','O3','CO']
        writer = csv.writer(csvFile)
        writer.writerow(row)
        for i in range(len(AQI_PM25)):
            my = [AQI_PM25[i], AQI_PM10[i], AQI_SO2[i], AQI_NO2[i], AQI_O3[i], AQI_CO[i]]
            writer.writerow(my)
        csvFile.close()
    
months = [25, 30, 31,  31, 30, 31, 30, 31,31,28,31,19]
monthlyAQI = np.zeros(12)

days = 0
for i in range(np.size(months, 0)):
    X = AQI[days:days+months[i]]
    a = np.nonzero(X)
    monthlyAQI[i] = np.mean(X[a])
    days = days + months[i]

print(monthlyAQI)
print(np.mean(monthlyAQI))


def connectpoints(x,y,p1,p2):
    x1, x2 = x[p1], x[p2]
    y1, y2 = y[p1], y[p2]
    plt.plot([x1,x2],[y1,y2],'k-')
#Plot graph of monthly data points
import matplotlib.pyplot as plt

x = np.array(['May18','June18','July18','Aug18','Sept18','Oct18','Nov18','Dec18','Jan19','Feb19','March19','April19'])
xa = np.array([0,1,2,3,4,5,6,7,8,9,10,11])
plt.xticks(np.arange(12), x)
y= list(monthlyAQI)
print(x)
print(y)
plt.xlabel('Months')
plt.ylabel('Monthly AQI')
for i in range(len(x)):
    plt.plot(x[i:i+2],y[i:i+2],'ro-')
plt.show()






