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
data = sio.loadmat('E:\python_scripts\Veh_Mapping\\n21_Timing_02.mat')

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
# print("size of cps = ",len(cps))
# print("size of ign = ",len(ign))
# print("size of time = ",len(time))



cpsAdvLevel = 4
cpsAdv=0
timeAdvDetected = 0
rpmFromAdv = np.zeros(len(cps))

cpsZeroLevel = -4
cpsZero=0
timeZeroDetected = 0
rpmFromZero = np.zeros(len(cps))

ignAngle = np.zeros(len(cps))

cpsZeroLevelDetected = False

diffTimeZeroDetected = 100000

dwellStartLevel = 4
dwellEndLevel = 4
timeDwellEndDetected = 0
dwellStartDetected = False
dwellEndDetected = False

minZeroLevel = 0
timeMinZeroLevel = 0

for i in range(len(cps)):

	#	rpm calculation: start
	if i > 0:
		rpmFromAdv[i] = rpmFromAdv[i - 1]
		rpmFromZero[i] = rpmFromZero[i - 1]
		ignAngle[i] = ignAngle[i - 1]
	if(cps[i] > cpsAdvLevel):
		cpsAdv = cpsAdv + 1;
		if((cpsAdvLevelDetected == False)):
			if (cpsAdv > 1):
				diffTimeAdvDetected = time[i] - timeAdvDetected
				rpmFromAdv[i] = 60/diffTimeAdvDetected
			timeAdvDetected = time[i]
		cpsAdvLevelDetected = True
	else:
		cpsAdvLevelDetected = False


	if (cps[i] < cpsZeroLevel):
		cpsZero = cpsZero + 1;
		if((cpsZeroLevelDetected == False)):
			if (cpsZero > 1):
				diffTimeZeroDetected = time[i] - timeZeroDetected
				rpmFromZero[i] = 60/diffTimeZeroDetected
			timeZeroDetected = time[i]		
		if(minZeroLevel > cps[i]):
			minZeroLevel = cps[i]
			timeMinZeroLevel = time[i]			
		cpsZeroLevelDetected = True
	else:
		if(cpsZeroLevelDetected == True):
			# print("timeMinZeroLevel = ",timeMinZeroLevel,"\n")
			ignAngle[i] = 360*(timeMinZeroLevel - timeDwellEndDetected)/diffTimeZeroDetected
			minZeroLevel = 0
		cpsZeroLevelDetected = False

	#	rpm calculation: end


	#	dwell detection: start
	if 1:
		if(ign[i] < dwellStartLevel):
			dwellStartDetected = True
		else:
			dwellStartDetected = False
		if(ign[i] > dwellEndLevel):
			if(dwellEndDetected == False):
				timeDwellEndDetected = time[i]
			dwellEndDetected = True
		else:
			dwellEndDetected = False
	#	dwell detection: end


if 1:
	if 0:		# decide whether to plot only cps and ign or rpm also
		plt.figure()
		plt.plot(time, cps, time, ign,  time, ignAngle)
		plt.xlabel('time')
		plt.ylabel('voltage')
	else:
		fig, ax1 = plt.subplots()
		ax2 = ax1.twinx()
		ax1.plot(time, cps, time, ign)
		# ax2.plot(time,rpmFromAdv, '-r', time,rpmFromZero,'-m')
		ax2.plot(time,ignAngle,'-r')
		# plt.xlabel('time')
		# plt.ylabel('voltage')		
	plt.grid()	
	if 1:		# decide whether to show the plot or save the file. 
		plt.show()
	else:		
		# pylab.savefig('n21_data_3.png')
		pass



