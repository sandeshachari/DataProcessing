#!/usr/bin/python

"""
CPS:	Single Pip
Ign:	TCI
Filter used in Pico:	10 kHz for both channels
"""

import scipy.io as sio
import pylab
import numpy as np
import matplotlib.pyplot as plt

# Write simple module for level detection and thus calculate the rpm


# data = sio.loadmat('E:\python_scripts\Veh_Mapping\\n21_data\\n21_data_1.mat')
data = sio.loadmat('E:\python_scripts\Veh_Mapping\\n21_data_1.mat')

if 0:	
	print("type of data = " ,type(data))
	print("size of A: ",len(data['A']))
	print("size of B: ",len(data['B']))
	print("\n\n\n")
	print(data)
	print("\n\n\n")
	# print("Data in dict: ", data['B'])

minDatapoints = min(len(data['A']),len(data['B']))
cpsRaw = data['A']
cps = cpsRaw[0:minDatapoints]
ignRaw = data['B']
ign = ignRaw[0:minDatapoints]
timeInterval = data['Tinterval']
timeStart = data['Tstart']

time = np.zeros(minDatapoints)
for i in range(minDatapoints):
	time[i] = timeStart*0 + i*timeInterval
print("size of cps = ",len(cps))
print("size of ign = ",len(ign))
print("size of time = ",len(time))

plt.figure()
plt.plot(time, cps, time, ign)
plt.xlabel('time')
plt.ylabel('voltage')
plt.grid()
plt.show()

# pylab.savefig('n21_data_3.png')

