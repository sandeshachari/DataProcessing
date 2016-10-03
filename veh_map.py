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
from colorama import Fore
import cmd
import click
import os
import subprocess
import tempfile
from parameters import *
import single_dual_pip,multi_pip



gTime = []	
gCps = []
gIgn = []
gRpm = []


class VehMap(cmd.Cmd):
	prompt = '{}VehMap: {}'.format(Fore.GREEN,Fore.WHITE)
	


	def do_EOF(self,line):
		""" End of File: Successfully terminates the custom shell"""
		return True

	def do_exit(self,line):
		""" exit: Successfully terminates the custom shell"""		
		return True

	def do_set_config_params(self,line):	
		subprocess.Popen(['subl','-w','set_params.txt']).wait()
		# subprocess.Popen(['notepad.exe','set_params.txt']).wait()		

		numLines = sum(1 for line in open('set_params.txt'))

		# print 'numLines = ',numLines

		f = open(r'set_params.txt','r');
		filedata = f.read()
		f.seek(0)
		
		if not params:
			for i in range(0,numLines):
				params.append(str.split(f.readline())[0])
		else:
			for i in range(0,len(params)):
				params[i] = str.split(f.readline())[0]

		

		# print 'params = ',params
		# print 'total teeth = ', paramTotalTeeth	
		pass


		


	def do_reset_config_params(self,line):
		autoLevelDetection = True
		cpsAdvLevel = 4
		cpsZeroLevel = -4
		dwellStartLevel = 4
		dwellEndLevel = 4
		injStartLevel = 3
		injEndLevel = 3
		cdiIgnDetectionLevel = -3
		injTech = 'carb'
		cpsType = 'single_pip_tci'
		nTeeth = 12
		nMissingTeeth = 3
		cpsChannel = 'A'
		ignChannel = 'B'
		injChannel = 'C'
		fileName = 'single_pip/N21_Timing_02.mat'


	def do_print_temp(self,line):
		print 'total teeth = ', params[10]


	def do_get_avg_outputs(self,line):		
		global gTime,gCps,gIgn,gRpm
		# global cpsType

		# print 'params = ',params


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

		# print 'cpsType in veh_map is = ',cpsType
		# print 'cpsChannel = ',cpsChannel
		

		# nTeeth = paramTotalTeeth
		# nMissingTeeth = paramTotalMissingTeeth

		# Pico channels setting
		# cpsChannel = paramCpsChannel
		# ignChannel = paramIgnChannel
		# injChannel = paramInjChannel



			
		if 0:
			cpsType = raw_input('\nEnter the type of cps and ign (single_pip_tci/single_pip_cdi/dual_pip_tci/dual_pip_cdi/multi_pip_tci/multi_pip_cdi): ')
			if cpsType == 'single_pip_tci' or cpsType == 'dual_pip_tci' or cpsType == 'single_pip_cdi' or cpsType == 'dual_pip_cdi' or cpsType == 'multi_pip_tci' or cpsType == 'multi_pip_cdi':
				print '\nCps type is: ', cpsType ,'\n'
			else:
				raise ValueError('Pls enter the valid input')
				sys.exit(1)
		else:
			# cpsType = 'multi_pip_tci'		
			# print '\nCps type is: ', cpsType ,'\n'	
			pass
		


		# Configurable parameters: start
		# cpsAdvLevel = paramCpsAdvLevel
		# cpsZeroLevel = paramCpsZeroLevel

		# dwellStartLevel = paramDwellStartLevel
		# dwellEndLevel = paramDwellEndLevel
		# cdiIgnDetectionLevel = paramCdiIgnDetectionLevel

		# Configurable parameters: end

		if cpsType == 'single_pip_tci' or cpsType == 'dual_pip_tci' or cpsType == 'single_pip_cdi' or cpsType == 'dual_pip_cdi':
			# call single_dual_pip
			single_dual_pip.single_dual_pip_processing()
		else:
			# call multi_pip	
			multi_pip.multi_pip_processing()
		return False

	# if 0:
	
	# @click.option('--entity','-m',click.Choice(['cps','ign','rpm']),multiple=True)
	# @click.option('--entity','-m',click.Choice(['cps_voltage','ign_voltage','inj_voltage']),multiple=True)	
	# @click.option('--entity','-m',multiple=True)	
	@click.command()
	@click.option('--count',default=1,help='number of greetings')
	@click.pass_context
	def do_plot_data(self,count):
		
		print 'Hello', count
		# single_dual_pip.single_dual_pip_plot()
		# multi_pip.multi_pip_plot(())
		# print entity
		pass


	def help_get_avg_outputs(self):
		print '\nMethod to extract the map from the given input data.\nIt has two arguments 1. cps_type  2. address'
		print 'cps_type = single_pip_tci/dual_pip_tci/single_pip_cdi/dual_pip_cdi'
		print 'address = Address of .mat file generated from pico data.\n'


	def postsmd(stop,line):
		print 'Exiting...'
		stop = False


def cli():	
	#""" Something """
	# print cps_type, '\n', address
	print '{}Note: Pls make sure that \n{}1. Pico data is filtered with at least 10kHz. \n2. It is stored in the .mat file.' \
	'\n3. Ign/Inj angle is calculated from the minimum of zero pulse.\n'.format(Fore.CYAN,Fore.WHITE)

	VehMap().cmdloop()    


if __name__ == '__main__':
    print ''
    # VehMap(cps_type,address).cmdloop()
    cli(	)
