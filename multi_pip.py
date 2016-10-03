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

gTime = []	
gCps = []
gIgn = []
gRpm = []

def multi_pip_processing():
	global cpsType,cpsAdvLevel,cpsZeroLevel,dwellStartLevel,dwellEndLevel,injStartLevel,injEndLevel,cdiIgnDetectionLevel,nTeeth,nMissingTeeth
	global autoLevelDetection,injTech
	global cpsChannel,ignChannel,injChannel

	# print 'params in multi_pip is = ',params 

	autoLevelDetection = (bool)(params[0])
	cpsAdvLevel = (int)(params[1])
	cpsZeroLevel = (int)(params[2])
	dwellStartLevel = (int)(params[3])
	dwellEndLevel = (int)(params[4])
	injStartLevel = (int)(params[5])
	injEndLevel = (int)(params[6])
	cdiIgnDetectionLevel = (int)(params[7])
	injTech = (params[8])
	cpsType = (params[9])
	nTeeth = (int)(params[10])
	nMissingTeeth = (int)(params[11])
	cpsChannel = params[12]
	ignChannel = params[13]
	injChannel = params[14]
	fileName = params[15]

	# print 'cpsType in multipip is: ',cpsType

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
			# data = sio.loadmat('E:\python_scripts\Veh_Mapping\multi_pip\\glamour_fi_data_2.mat')
			data = sio.loadmat(fileName)			
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

	# print(data)
	# print 'nTeeth = ',nTeeth
	# print 'nMissingTeeth = ',nMissingTeeth

	minDatapoints = min(len(data['A']),len(data['B']),len(data['C']))
	cpsRaw = data[cpsChannel]
	# print 'length of cps = ', len(cps)
	cps = cpsRaw[0:minDatapoints]
	# print 'length of cps = ', len(cps)
	gCps = cps
	# print 'gCps_1:\n',gCps
	ignRaw = data[ignChannel]
	ign = ignRaw[0:minDatapoints]
	gIgn = ign

	injRaw = data[injChannel]
	inj = injRaw[0:minDatapoints]
	gInj = inj

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

	injAngle = np.zeros(len(cps))
	injAngleList = []

	cpsZeroLevelDetected = False

	diffTimeZeroDetected = 100000

	timeDwellEndDetected = 0
	dwellStartDetected = False
	dwellEndDetected = False

	minZeroLevel = 0
	timeMinZeroLevel = 0

	injEndDetected = False
	injStartDetected = False



	# each tooth time = 1/nTeeth
	# missing tooth time = (nMissingTeeth + 1)/nTeeth

	rpmFromAdvMissingTooth = np.zeros(len(cps))
	diffTimeAdvDetectedOld = 0.000001	#0.000000000000001
	timeAdvMissingToothDetected = 0
	timeAdvMissingToothDetectedOld = 0
	cpsAdvMissingTooth = 0

	rpmFromZeroMissingTooth = np.zeros(len(cps))
	diffTimeZeroDetectedOld = 0.000001			#0.000000000000001
	timeZeroMissingToothDetected = 0
	timeZeroMissingToothDetectedOld = 0
	cpsZeroMissingTooth = 0

	maxAdvLevel = 0
	timeMaxAdvLevel = 0

	diffTimeAdvMissingToothDetected = 0

	cpsAdvLevelDetected = False
	missingToothDetected = False

	itSparked = False
	itInjected = False

	timeDwellStartDetected = 0

	timeInjStartDetected = 0

	rpmFromAdvMissingToothList = []
	rpmFromZeroMissingToothList = []
	timeDwellOnList = []
	timeInjOnList = []

	entered =  0

	for i in range(len(cps)):		#minDatapoints
		time[i] = timeStart*0 + i*timeInterval

	# plt.plot(time,cps)
	# plt.show()

	for i in range(len(cps)):
		if i > 0:
			rpmFromAdvMissingTooth[i] = rpmFromAdvMissingTooth[i - 1] 
			rpmFromZeroMissingTooth[i] = rpmFromZeroMissingTooth[i - 1] 
			ignAngle[i] = ignAngle[i - 1]
		if cps[i] > cpsAdvLevel:
			if cpsAdvLevelDetected == False:
				cpsAdv = cpsAdv + 1
				diffTimeAdvDetected = time[i] - timeAdvDetected
				timeAdvDetected = time[i]		
				if cpsAdv > 2:
					if diffTimeAdvDetected/diffTimeAdvDetectedOld > nMissingTeeth:
						missingToothDetected = True
						cpsAdvMissingTooth = cpsAdvMissingTooth + 1
						timeAdvMissingToothDetected = time[i]					
						if cpsAdvMissingTooth > 1:
							diffTimeAdvMissingToothDetected = timeAdvMissingToothDetected - timeAdvMissingToothDetectedOld
							rpmFromAdvMissingTooth[i] = 60/diffTimeAdvMissingToothDetected 
							missingToothIndicationForCdiIgn = True
							rpmFromAdvMissingToothList.append(round(rpmFromAdvMissingTooth[i],2))
						timeAdvMissingToothDetectedOld = timeAdvMissingToothDetected 					
					else:
						# missingToothDetected = False
						pass
				diffTimeAdvDetectedOld = diffTimeAdvDetected
			if(maxAdvLevel < cps[i]) and missingToothDetected == True:
				maxAdvLevel = cps[i]
				timeMaxAdvLevel = time[i]				
			cpsAdvLevelDetected = True
		else:				
			if missingToothDetected == True and cpsAdvMissingTooth > 1:
				if itSparked == True:
					if cpsType == 'multi_pip_tci':
						ignAngle[i] = 360*(timeMaxAdvLevel - timeDwellEndDetected)/diffTimeAdvMissingToothDetected
					else:
						ignAngle[i] = 360*(timeMaxAdvLevel - timeCdiIgnDetected)/diffTimeAdvMissingToothDetected

					ignAngleList.append(round(ignAngle[i],2)) 
					itSparked = False
				if itInjected == True:
					injAngle[i] = 360*(timeMaxAdvLevel - timeInjEndDetected)/diffTimeAdvMissingToothDetected
					injAngleList.append(round(injAngle[i],2)) 								
					itInjected = False
			maxAdvLevel = 0				
			cpsAdvLevelDetected = False
			missingToothDetected = False


		if cps[i] < cpsZeroLevel:
			if cpsZeroLevelDetected == False:
				cpsZero = cpsZero + 1
				diffTimeZeroDetected = time[i] - timeZeroDetected
				timeZeroDetected = time[i]		
				if cpsZero > 2:
					if diffTimeZeroDetected/diffTimeZeroDetectedOld > nMissingTeeth:
						cpsZeroMissingTooth = cpsZeroMissingTooth + 1
						timeZeroMissingToothDetected = time[i]					
						if cpsZeroMissingTooth > 1:
							rpmFromZeroMissingTooth[i] = 60/(timeZeroMissingToothDetected - timeZeroMissingToothDetectedOld)
							rpmFromZeroMissingToothList.append(round(rpmFromZeroMissingTooth[i],2))
						timeZeroMissingToothDetectedOld = timeZeroMissingToothDetected 
				diffTimeZeroDetectedOld = diffTimeZeroDetected
			cpsZeroLevelDetected = True
		else:
			cpsZeroLevelDetected = False	

			#	dwell detection: start
		if 1:
			if cpsType == 'multi_pip_tci':
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
			else:
				if ign[i] < cdiIgnDetectionLevel and cdiIgnDetected == False and missingToothIndicationForCdiIgn == True: 
					timeCdiIgnDetected = time[i]
					cdiIgnDetected = True	
					missingToothIndicationForCdiIgn = False 
				else:
					cdiIgnDetected = False
			# dwell detection: end

			# fi detection: start
		if 1:				
			if(inj[i] < injStartLevel):
				if injStartDetected == False:
					timeInjStartDetected = time[i]
				injStartDetected = True			
			else:
				injStartDetected = False
			if(inj[i] > injEndLevel):
				if(injEndDetected == False):
					entered = 34
					itInjected = True
					timeInjEndDetected = time[i]
					timeInjOnList.append(round((timeInjEndDetected - timeInjStartDetected)*1000,2))
				injEndDetected = True
			else:
				injEndDetected = False
			# fi detection: end

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
			# ax2.plot(time,rpmFromAdvMissingTooth, '-r', time,rpmFromZeroMissingTooth,'-m')
			ax2.plot(time,ignAngle,'-r')
			# plt.xlabel('time')
			# plt.ylabel('voltage')		
		plt.grid()	
		if 1:		# decide whether to show the plot or save the file. 
			plt.show()
		else:		
			pylab.savefig('\single_pip\\n21_data_3.png')
			pass


	avgRpm = round(np.array(rpmFromAdvMissingToothList[1:len(rpmFromAdvMissingToothList)-1]).mean(),2)
	rpmStdDev = round(np.array(rpmFromAdvMissingToothList[1:len(rpmFromAdvMissingToothList)-1]).std(),2)	

	avgIgnAngle = round(np.array(ignAngleList[3:len(ignAngleList)-1]).mean(),2)
	ignAngleStdDev = round(np.array(ignAngleList[3:len(ignAngleList)-1]).std(),2)	

	avgInjAngle = round(np.array(injAngleList[3:len(injAngleList)-1]).mean(),2)
	injAngleStdDev = round(np.array(injAngleList[3:len(injAngleList)-1]).std(),2)	

	avgInjOnTime = round(np.array(timeInjOnList[3:len(timeInjOnList)-1]).mean(),2)	
	injOnTimeStdDev = round(np.array(timeInjOnList[3:len(timeInjOnList)-1]).std(),2)


	print '\n {0}{1:15}\t\t\t{2:7}\t\t\t{3:7}'.format(Fore.CYAN,'Entity','Average','Std dev')
	print ' {0}{1:15}\t\t\t{2:.2f}\t\t\t{3:.2f}'.format(Fore.WHITE,'Rpm',avgRpm,rpmStdDev)
	print ' {0}{1:15}\t\t\t{2:.2f}\t\t\t{3:.2f}'.format(Fore.WHITE,'Ign Angle(degrees)',avgIgnAngle,ignAngleStdDev)

	# # 1 space 4 tabs, 1 space 8 tabs
	# print '\n\nEntity 				Average 					Std dev'
	# print '\nRpm 				', avgRpm,'						',rpmStdDev 
	# print '\nIgn Angle (degrees)		', avgIgnAngle,'						',ignAngleStdDev, 
	# print '\nInj Angle (degrees)		', avgInjAngle,'						',injAngleStdDev, 

	if cpsType == 'multi_pip_tci':
		avgDwellOnTime = round(np.array(timeDwellOnList[3:len(timeDwellOnList)-1]).mean(),2)	
		dwellOnTimeStdDev = round(np.array(timeDwellOnList[3:len(timeDwellOnList)-1]).std(),2)
		# print '\nAverage dwell on time = ', avgDwellOnTime,'ms', '		Std dev in dwell on time = ',dwellOnTimeStdDev,'ms'	
		# print '\nDwell on time (ms)		', avgDwellOnTime,'						',dwellOnTimeStdDev, 
		print ' {0}{1:15}\t\t\t{2:.2f}\t\t\t{3:.2f}'.format(Fore.WHITE,'Dwell on time (ms)',avgDwellOnTime,dwellOnTimeStdDev)


	# print '\nInj on time (ms)		', avgInjOnTime,'						',injOnTimeStdDev, 
	print ' {0}{1:15}\t\t\t{2:.2f}\t\t\t{3:.2f}'.format(Fore.WHITE,'Inj on time (ms)',avgInjOnTime,injOnTimeStdDev)



	mappingFailed = False
	if rpmStdDev > 150 or math.isnan(rpmStdDev):
		print '\n\nSomething went wrong with the rpm. Change the zero detection level if necessary.'
		mappingFailed = True
	if ignAngleStdDev > 5 or math.isnan(ignAngleStdDev):
		print '\n\nSomething went wrong with the ign angle. Change the ign detection level if necessary.'
		mappingFailed = True
	if injAngleStdDev > 5 or math.isnan(injAngleStdDev):
		print '\n\nSomething went wrong with the inj angle. Change the inj detection level if necessary.'
		mappingFailed = True	
	if dwellOnTimeStdDev > 5 or math.isnan(dwellOnTimeStdDev) and  cpsType == 	'multi_pip_tci':
		print '\n\nSomething went wrong with the dwell on time. Change the dwell detection level if necessary.'
		mappingFailed = True		
	if injOnTimeStdDev > 5 or math.isnan(injOnTimeStdDev):
		print '\n\nSomething went wrong with the inj on time. Change the inj detection level if necessary.'
		mappingFailed = True	

	if mappingFailed == False:
		print '\n\nInput data looks good. Successfully completed mapping.\n\n'	


	# print '\n\n\n entered = ', entered	

	# plt.plot(time,cps,time,ign,time,inj)
	# plt.grid()
	# plt.show()

def multi_pip_plot(output_list):
	global gTime,gCps,gIgn,gRpm
	plot_list = output_list		
	
	if 0:
		global gTime,gCps,gIgn,gRpm	
		plt.plot(gTime,gRpm)
		plt.grid()
		plt.show()
	else:
		j=0
		for i in range(0,len(output_list)):
			if output_list[i] == 'cps_voltage':
				plot_list[j] = gCps
			elif output_list[i] == 'ign_voltage':
				plot_list[j] = gIgn
			elif output_list[i] == 'inj_voltage':
				plot_list[j] = gInj
			j = j + 1

		for entity in plot_list:
			plt.plot(gTime,entity,label=entity)

		plt.legend()
		plt.grid()
		plt.show()

