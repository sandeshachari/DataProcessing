"""
CPS:	Single Pip
Ign:	TCI
Filter used in Pico:	10 kHz for both channels

cases:
1. 	Single pip, Ign in each cycle
2. 	Dual pip, Ign in each cycle
3. 	Multi pip, Ign in each thermo-cycle, fi in each thermo-cycle  <-- FI
"""

#!/usr/bin/python

import scipy.io as sio
import pylab
import numpy as np
import matplotlib.pyplot as plt
import sys
import math


if 1:
	cpsType = raw_input('\nEnter the type of cps and ign (single_pip_tci/dual_pip_tci/single_pip_cdi/dual_pip_cdi): ')
	if cpsType == 'single_pip_tci' or cpsType == 'dual_pip_tci' or cpsType == 'single_pip_cdi' or cpsType == 'dual_pip_cdi':	# or cpsType == 'multi_pip':
		print '\nCps type is: ', cpsType ,'\n'
		print 'Note: Pls make sure that \n1. Pico data is filtered with at least 10kHz. \n2. It is stored in the .mat file.' \
		'\n3. Ign/Inj angle is calculated from the minimum of zero pulse.\n'

		# sys.exit(1)
	else:
		raise ValueError('Pls enter the valid input')
		sys.exit(1)
else:
	cpsType = 'dual_pip_cdi'		

# Write simple module for level detection and thus calculate the rpm


if 1:
	try:
		fileAddress = raw_input('Enter the address of the .mat file: ')
		data = sio.loadmat(fileAddress)
	except IOError:
		print 'Wrong address.'
		sys.exit(1)
else:		
	try:
		data = sio.loadmat('E:\python_scripts\Veh_Mapping\dual_pip\\dual_pip_data_1.mat')
	except:
		print 'No such file in directory.'
		sys.exit(1)

if 0:	
	print "type of data = " ,type(data)
	print "size of A: ",len(data['A'])
	print "size of B: ",len(data['B'])
	print "\n\n\n"
	print data
	print "\n\n\n"
	# print "Data in dict: ", data['B']

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


# Configurable parameters: start
cpsAdvLevel = 4
cpsZeroLevel = -4

dwellStartLevel = 4
dwellEndLevel = 4
cdiIgnDetectionLevel = -6

# Configurable parameters: end

cpsAdv=0
timeAdvDetected = 0
rpmFromAdv = np.zeros(len(cps))

cpsZero=0
timeZeroDetected = 0
rpmFromZero = np.zeros(len(cps))

ignAngle = np.zeros(len(cps))
ignAngleList = []
timeDwellOnList = []

cpsZeroLevelDetected = False
cpsAdvLevelDetected = False

diffTimeZeroDetected = 100000
diffTimeZeroDetectedOld = 100000
diffTimeZerotoZeroDetected = 100000

timeDwellStartDetected = 0
timeDwellEndDetected = 0
dwellStartDetected = False
dwellEndDetected = False

minZeroLevel = 0
timeMinZeroLevel = 0

cdiIgnDetected = False
timeDwellStartDetected = 0
cpsAdvForIgnDetected = False
diffTimeZeroToZeroDetected = 0
timeCdiIgnDetected = 0
itSparked = False
avgDwellOnTime = 0

rpmFromZeroList = []
entered = 0
cpsZeroBig = 0

for i in range(len(cps)):

	#	rpm calculation: start
	if i > 0:
		rpmFromAdv[i] = rpmFromAdv[i - 1]
		rpmFromZero[i] = rpmFromZero[i - 1]
		ignAngle[i] = ignAngle[i - 1]
	if(cps[i] > cpsAdvLevel):
		cpsAdv = cpsAdv + 1;
		if((cpsAdvLevelDetected == False)):
			if cpsType == 'single_pip_tci' or cpsType == 'single_pip_cdi':
				if (cpsAdv > 1):
					diffTimeAdvDetected = time[i] - timeAdvDetected
					rpmFromAdv[i] = 60/diffTimeAdvDetected
				timeAdvDetected = time[i]
			elif cpsType == 'dual_pip':
				# diffTimeAdvDetected = time[i] - timeAdvDetected
				# if(cpsAdv > 2):
				# 	if int(diffTimeAdvDetected/diffTimeAdvDetectedOld) == 0:
				# 		# Small pip is ignored
				# 		rpmFromAdv[i] = 60/(diffTimeAdvDetected + diffTimeAdvDetectedOld)
				# timeAdvDetected = time[i]
				# diffTimeAdvDetectedOld = diffTimeAdvDetected
				pass
		cpsAdvForIgnDetected = True
		cpsAdvLevelDetected = True
	else:
		cpsAdvLevelDetected = False


	if (cps[i] < cpsZeroLevel):
		if((cpsZeroLevelDetected == False)):
			cpsZero = cpsZero + 1;
			if cpsType == 'single_pip_tci' or cpsType == 'single_pip_cdi':
				if (cpsZero > 1):
					diffTimeZeroDetected = time[i] - timeZeroDetected
					rpmFromZero[i] = 60/diffTimeZeroDetected			
					rpmFromZeroList.append(round(rpmFromZero[i],2))
					if cpsZero == 3:
						cpsZeroLevel = -(int)((3 + 2*((float)(rpmFromZero[i]) - 300)/2700)*(rpmFromZero[i] < 3000) + 4*(rpmFromZero[i] >= 3000))
						print '\ncpsZeroLevel = ', cpsZeroLevel						
						if cpsType == 'single_pip_tci':
							dwellStartLevel = 4
							dwellEndLevel = 4
						else:
							cdiIgnDetectionLevel = -(int)((2 + 4*((float)(rpmFromZero[i]) - 300)/2700)*(rpmFromZero[i] < 3000)	\
							+ 6*(rpmFromZero[i] >= 3000))	
							print '\ncdiIgnDetectionLevel = ',cdiIgnDetectionLevel
						entered = 34
				timeZeroDetected = time[i]		
			else:
				diffTimeZeroDetected = time[i] - timeZeroDetected
				if(cpsAdv > 2):
					if int(diffTimeZeroDetected/diffTimeZeroDetectedOld) == 0:
						# Small pip is ignored
						cpsZeroBig = cpsZeroBig + 1
						rpmFromZero[i] = 60/(diffTimeZeroDetected + diffTimeZeroDetectedOld)
						rpmFromZeroList.append(round(rpmFromZero[i],2))
						diffTimeZeroToZeroDetected = diffTimeZeroDetected + diffTimeZeroDetectedOld
						if cpsZeroBig == 2:
							cpsZeroLevel = -(int)((3 + 2*((float)(rpmFromZero[i]) - 300)/2700)*(rpmFromZero[i] < 3000) + 4*(rpmFromZero[i] >= 3000))
							if cpsType == 'dual_pip_tci':
								dwellStartLevel = 4
								dwellEndLevel = 4
							else:
								cdiIgnDetectionLevel = -(int)((3 + 4*((float)(rpmFromZero[i]) - 300)/2700)*(rpmFromZero[i] < 3000)	\
								+ 6*(rpmFromZero[i] >= 3000))	
								# cdiIgnDetectionLevel = -6		
							print '\ncpsZeroLevel = ', cpsZeroLevel
							print '\ncdiIgnDetectionLevel = ',cdiIgnDetectionLevel

						smallPip = False
					else:
						smallPip = True
				timeZeroDetected = time[i]
				diffTimeZeroDetectedOld = diffTimeZeroDetected

		if cpsType == 'single_pip_tci' or cpsType == 'single_pip_cdi' or \
		((cpsType == 'dual_pip_tci' or cpsType == 'dual_pip_cdi') and cpsZero > 2 and smallPip == False):
			if(minZeroLevel > cps[i]):
				minZeroLevel = cps[i]
				timeMinZeroLevel = time[i]			
		cpsZeroLevelDetected = True
	else:
		if(cpsZeroLevelDetected == True):
			# print("timeMinZeroLevel = ",timeMinZeroLevel,"\n")
			if cpsType == 'single_pip_tci':
				ignAngle[i] = 360*(timeMinZeroLevel - timeDwellEndDetected)/diffTimeZeroDetected	
			elif cpsType == 'dual_pip_tci':
				ignAngle[i] = 360*(timeMinZeroLevel - timeDwellEndDetected)/diffTimeZerotoZeroDetected	
			elif cpsType == 'single_pip_cdi':
				ignAngle[i] = 360*(timeMinZeroLevel - timeCdiIgnDetected)/diffTimeZeroDetected											
			elif cpsType == 'dual_pip_cdi':
				ignAngle[i] = 360*(timeMinZeroLevel - timeCdiIgnDetected)/diffTimeZeroToZeroDetected

			ignAngleList.append(round(ignAngle[i],2))
			minZeroLevel = 0
			if itSparked == False and (cpsType == 'single_pip_tci' or cpsType == 'dual_pip_tci'):
				print 'ign miss at ',time[i],'ms'
			itSparked = False
		cpsZeroLevelDetected = False

	#	rpm calculation: end

	#	dwell detection: start
	if 1:
		if cpsType == 'single_pip_tci' or cpsType == 'dual_pip_tci':
			if(ign[i] < dwellStartLevel):
				itSparked = True
				if dwellStartDetected == False:
					timeDwellStartDetected = time[i]
				dwellStartDetected = True			
			else:
				dwellStartDetected = False
			if(ign[i] > dwellEndLevel):
				if(dwellEndDetected == False):
					timeDwellEndDetected = time[i]
					timeDwellOnList.append(round((timeDwellEndDetected - timeDwellStartDetected)*1000,2))
				dwellEndDetected = True
			else:
				dwellEndDetected = False
		elif cpsType == 'single_pip_cdi' or cpsType == 'dual_pip_cdi':
			if ign[i] < cdiIgnDetectionLevel and cpsAdvForIgnDetected == True:
				cpsAdvForIgnDetected = False
				if cdiIgnDetected == False:
					timeCdiIgnDetected = time[i]
				cdiIgnDetected = True	 
			else:
				cdiIgnDetected = False
	#	dwell detection: end


if 0:
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
		# ax2.plot(time,ignAngle,'-r')
		ax2.plot(time,rpmFromZero,'-r')	
		# plt.xlabel('time')
		# plt.ylabel('voltage')		
	plt.grid()	
	if 1:		# decide whether to show the plot or save the file. 
		plt.show()
	else:		
		pylab.savefig('\single_pip\\n21_data_3.png')
		pass


dwellOnTimeStdDev = 0


avgRpm = round(np.array(rpmFromZeroList[1:len(rpmFromZeroList)-1]).mean(),2)
rpmStdDev = round(np.array(rpmFromZeroList[1:len(rpmFromZeroList)-1]).std(),2)	

avgIgnAngle = round(np.array(ignAngleList[3:len(ignAngleList)-1]).mean(),2)
ignAngleStdDev = round(np.array(ignAngleList[3:len(ignAngleList)-1]).std(),2)	


# print '\nRpm:\n',rpmFromZeroList[1:len(rpmFromZeroList)-1]		
# print '\nIgn angles in degree (before zero pulse min point):\n',ignAngleList[1:len(ignAngleList)-1]

# 1 space 4 tabs, 1 space 8 tabs
print '\n\nEntity 				Average 					Std dev'
print '\nRpm 				', avgRpm,'						',rpmStdDev 
print 'Ign Angle (degrees)		', avgIgnAngle,'						',ignAngleStdDev, 

if cpsType == 'single_pip_tci' or cpsType == 'dual_pip_tci':
	avgDwellOnTime = round(np.array(timeDwellOnList[1:len(timeDwellOnList)-1]).mean(),2)	
	dwellOnTimeStdDev = round(np.array(timeDwellOnList[1:len(timeDwellOnList)-1]).std(),2)
	# print '\nAverage dwell on time = ', avgDwellOnTime,'ms', '		Std dev in dwell on time = ',dwellOnTimeStdDev,'ms'	
	print '\nDwell on time (ms)		', avgDwellOnTime,'						',dwellOnTimeStdDev, 

mappingFailed = False
if rpmStdDev > 150 or math.isnan(rpmStdDev):
	print '\n\nSomething went wrong with the rpm. Change the zero detection level if necessary.'
	mappingFailed = True
if ignAngleStdDev > 5 or math.isnan(ignAngleStdDev):
	print '\n\nSomething went wrong with the ign angle. Change the ign detection level if necessary.'
	mappingFailed = True

if mappingFailed == False:
	print '\n\nInput data looks good. Successfully completed mapping.'


# print '\n\n\nentered = ',entered,	' cpsZero = ', cpsZero