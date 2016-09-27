import scipy.io as sio
import pylab
import numpy as np
import matplotlib.pyplot as plt
import sys
import math
from colorama import Fore
import cmd
import click
import os
import subprocess
import tempfile
from parameters import *
# import parameters


def single_dual_pip_processing():
	global cpsType,cpsAdvLevel,cpsZeroLevel,dwellStartLevel,dwellEndLevel,cdiIgnDetectionLevel
	print 'cpsType is: ',cpsType
	if 0:
		try:
			fileAddress = raw_input('Enter the address of the .mat file: ')
			data = sio.loadmat(fileAddress)
		except IOError:
			print 'Wrong address.'
			# sys.exit(1)
			return False
	else:		
		try:
			data = sio.loadmat('E:\python_scripts\Veh_Mapping\single_pip\\N21_Timing_02.mat')
			# data = sio.loadmat(address)				
		except:
			print 'No such file in directory.'
			# sys.exit(1)
			return False

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
	# print 'length of cps = ', len(cps)
	cps = cpsRaw[0:minDatapoints]
	# print 'length of cps = ', len(cps)
	gCps = cps
	# print 'gCps_1:\n',gCps
	ignRaw = data['B']
	ign = ignRaw[0:minDatapoints]
	gIgn = ign
	timeInterval = data['Tinterval']
	timeStart = data['Tstart']

	time = np.zeros(minDatapoints)
	gTime = time	

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

	# print 'length of cps = ', len(cps)

	for i in range(len(cps)):		#minDatapoints
		time[i] = timeStart*0 + i*timeInterval


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


	dwellOnTimeStdDev = 0


	avgRpm = round(np.array(rpmFromZeroList[1:len(rpmFromZeroList)-1]).mean(),2)
	rpmStdDev = round(np.array(rpmFromZeroList[1:len(rpmFromZeroList)-1]).std(),2)	

	avgIgnAngle = round(np.array(ignAngleList[3:len(ignAngleList)-1]).mean(),2)
	ignAngleStdDev = round(np.array(ignAngleList[3:len(ignAngleList)-1]).std(),2)	


	# print '\nRpm:\n',rpmFromZeroList[1:len(rpmFromZeroList)-1]		
	# print '\nIgn angles in degree (before zero pulse min point):\n',ignAngleList[1:len(ignAngleList)-1]

	# 1 space 4 tabs, 1 space 8 tabs
	# print '\n\nEntity 				Average 					Std dev'
	# print '\nRpm 				', avgRpm,'						',rpmStdDev 
	# print 'Ign Angle (degrees)		', avgIgnAngle,'						',ignAngleStdDev, 

	print '\n {0}{1:15}\t\t\t{2:7}\t\t\t{3:7}'.format(Fore.CYAN,'Entity','Average','Std dev')
	print ' {0}{1:15}\t\t\t{2:.2f}\t\t\t{3:.2f}'.format(Fore.WHITE,'Rpm',avgRpm,rpmStdDev)
	print ' {0}{1:15}\t\t\t{2:.2f}\t\t\t{3:.2f}'.format(Fore.WHITE,'Ign Angle(degrees)',avgIgnAngle,ignAngleStdDev)

	if cpsType == 'single_pip_tci' or cpsType == 'dual_pip_tci':
		avgDwellOnTime = round(np.array(timeDwellOnList[1:len(timeDwellOnList)-1]).mean(),2)	
		dwellOnTimeStdDev = round(np.array(timeDwellOnList[1:len(timeDwellOnList)-1]).std(),2)
		# print '\nAverage dwell on time = ', avgDwellOnTime,'ms', '		Std dev in dwell on time = ',dwellOnTimeStdDev,'ms'	
		# print '\nDwell on time (ms)		', avgDwellOnTime,'						',dwellOnTimeStdDev, 
		print ' {0}{1:15}\t\t\t{2:.2f}\t\t\t{3:.2f}'.format(Fore.WHITE,'Dwell on time (ms)',avgDwellOnTime,dwellOnTimeStdDev)


	mappingFailed = False
	if rpmStdDev > 150 or math.isnan(rpmStdDev):
		print '\n\nSomething went wrong with the rpm. Change the zero detection level if necessary.\n\n'
		mappingFailed = True
	if ignAngleStdDev > 5 or math.isnan(ignAngleStdDev):
		print '\n\nSomething went wrong with the ign angle. Change the ign detection level if necessary.\n\n'
		mappingFailed = True

	if mappingFailed == False:
		print '\n\nInput data looks good. Successfully completed mapping.\n\n'

	gRpm = rpmFromZero
	# print 'shutters down.'
	plt.plot(time,rpmFromZero)#,time,ign)
	plt.grid()
	# plt.show()

