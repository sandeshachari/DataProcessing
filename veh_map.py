"""
CPS:	Single Pip
Ign:	TCI
Filter used in Pico:	10 kHz for both channels

cases:
1. 	Single pip, Ign in each cycle
2. 	Dual pip, Ign in each cycle
3. 	Multi pip, Ign in each thermo-cycle, fi in each thermo-cycle  <-- FI
"""
#E:\python_scripts\Veh_Mapping\dual_pip\dual_pip_data.mat
#!/usr/bin/python

import scipy.io as sio
import pylab
import numpy as np
import matplotlib.pyplot as plt
import sys


if 1:
	cpsType = raw_input('Enter the type of cps and ign (single_pip_tci/dual_pip_tci/single_pip_cdi/dual_pip_cdi): ')
	if cpsType == 'single_pip_tci' or cpsType == 'dual_pip_tci' or cpsType == 'single_pip_cdi' or cpsType == 'dual_pip_cdi':	# or cpsType == 'multi_pip':
		print '\nCps type is: ', cpsType ,'\n'
		print 'Note: Pls make sure that pico data should be filtered with at least 10kHz. \n      and it is stored in the .mat file.\n'
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

diffTimeZeroDetected = 100000
diffTimeZeroDetectedOld = 100000

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
cdiIgnDetectionLevel = -6	
timeCdiIgnDetected = 0
itSparked = False
avgDwellOnTime = 0

rpmFromZeroList = []

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
		cpsZero = cpsZero + 1;
		if((cpsZeroLevelDetected == False)):
			if cpsType == 'single_pip_tci' or cpsType == 'single_pip_cdi':
				if (cpsZero > 1):
					diffTimeZeroDetected = time[i] - timeZeroDetected
					rpmFromZero[i] = 60/diffTimeZeroDetected			
					rpmFromZeroList.append(round(rpmFromZero[i],2))

				timeZeroDetected = time[i]		
			else:
				diffTimeZeroDetected = time[i] - timeZeroDetected
				if(cpsAdv > 2):
					if int(diffTimeZeroDetected/diffTimeZeroDetectedOld) == 0:
						# Small pip is ignored
						rpmFromZero[i] = 60/(diffTimeZeroDetected + diffTimeZeroDetectedOld)
						rpmFromZeroList.append(round(rpmFromZero[i],2))
						diffTimeZeroToZeroDetected = diffTimeZeroDetected + diffTimeZeroDetectedOld
						smallPip = False
					else:
						smallPip = True
				timeZeroDetected = time[i]
				diffTimeZeroDetectedOld = diffTimeZeroDetected

		if cpsType == 'single_pip_tci' or cpsType == 'single_pip_cdi' or ((cpsType == 'dual_pip_tci' or cpsType == 'dual_pip_cdi') and cpsZero > 2 and smallPip == False):
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
				print 'ign miss at ',time[i]
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


avgRpm = round(np.array(rpmFromZeroList).mean(),2)
avgIgnAngle = round(np.array(ignAngleList[1:len(ignAngleList)-1]).mean(),2)

if cpsType == 'single_pip_tci' or cpsType == 'dual_pip_tci':
	avgDwellOnTime = round(np.array(timeDwellOnList[1:len(timeDwellOnList)-1]).mean(),2)
print '\nSuccessfully completed mapping.'
print '\nRpm:\n',rpmFromZeroList		
print '\nIgn angles in degree (before zero pulse):\n',ignAngleList[1:len(ignAngleList)-1]
if cpsType == 'single_pip_tci' or cpsType == 'dual_pip_tci':
	print '\nDwell on times (ms):\n',timeDwellOnList[1:len(timeDwellOnList)-1]
print '\n\nAverage rpm = ', avgRpm	
print '\nAverage ign angle = ',avgIgnAngle,'degrees'
if cpsType == 'single_pip_tci' or cpsType == 'dual_pip_tci':
	print '\nAverage dwell on time = ', avgDwellOnTime,'ms'



