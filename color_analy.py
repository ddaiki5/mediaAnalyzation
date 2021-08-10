import csv
import numpy as np
from scipy import linalg

samples = [[0, 0, 0], [255, 255, 255], [255, 0, 0], [255, 127, 0], [255, 255, 0],\
           [127, 255, 0], [0, 255, 0], [0, 255, 127], [0, 255, 255], [0, 127, 255],\
           [0, 0, 255], [127, 0, 255], [255, 0, 255], [255, 0, 127]]
l = []
word_list = []

#結果から各色彩の生起確率を求める

with open('result.csv') as f:
    reader = csv.reader(f)
    for row in reader:
        fl = [int(v)/12 for v in row[1:]]
        ll = [row[0], fl]
        word_list.append(row[0])
        l.append(ll)
l2 = []
l3 = [4 ,1, 6, 6, 1, 3, 3, 6, 2, 6, 1, 2] #読書量
V = []
with open('result2.csv', encoding='utf-8') as f:
    reader = csv.reader(f)
    for row in reader:
        fl = [int(v) for v in row[1:11]]
        l2.append(fl)
print(l2)
for k in range(0, 10):
    v = [0]*3
    a = [[0]*3]*3
    for i in range(0, 12):
        if l3[i]<4:   
            for j in range(0, 3):
                a[0][j] += samples[l2[i][k]-1][j]/7
        else:
            for j in range(0, 3):
                a[1][j] += samples[l2[i][k]-1][j]/5
        for j in range(0, 3):
                a[2][j] += samples[l2[i][k]-1][j]/12

    for i in range(0, 12):
        if l3[i]<4:   
            v[0] += (pow(samples[l2[i][k]-1][0]-a[0][0], 2) + pow(samples[l2[i][k]-1][1]-a[0][1], 2) + pow(samples[l2[i][k]-1][2]-a[0][2], 2))/7
        else:
            v[1] += (pow(samples[l2[i][k]-1][0]-a[0][0], 2) + pow(samples[l2[i][k]-1][1]-a[0][1], 2) + pow(samples[l2[i][k]-1][2]-a[0][2], 2))/5
        v[2] += (pow(samples[l2[i][k]-1][0]-a[0][0], 2) + pow(samples[l2[i][k]-1][1]-a[0][1], 2) + pow(samples[l2[i][k]-1][2]-a[0][2], 2))/12

    v = [round(v[0]/255/255, 4), round(v[1]/255/255,4), round(v[2]/255/255,4)]
    V.append(v)
aV=[0]*3
for i in range(0, 10):
    aV[0]+=V[i][0]/10
    aV[1]+=V[i][1]/10
    aV[2]+=V[i][2]/10
aV = [round(aV[0],4),round(aV[1],4),round(aV[2],4)]
print(V)
print(aV)












