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
#import parameters
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


	# @click.command()
	# # @click.option('--cps_type',prompt= 'Enter the type of cps and ign: ',help = 'single_pip_tci/dual_pip_tci/single_pip_cdi/dual_pip_cdi')
	# @click.option('--cps_type',prompt= 'Enter the type of cps and ign',type = click.Choice(['single_pip_tci','single_pip_cdi','dual_pip_tci','dual_pip_cdi']),help = 'single_pip_tci/dual_pip_tci/single_pip_cdi/dual_pip_cdi')	
	# @click.option('--address',prompt = 'Enter the address of the .mat file: ', help = 'Address of .mat file generated from pico data.')
	# cps_type = 'dual_pip_cdi'
	# address = 'dual_pip/dual_pip_data.mat'

	def do_set_config_params(self,line):	
		# os.startfile('parameters.py')			
		# parameters.init()
		# print 'paramInjTech in veh_map.py =',parameters.paramInjTech
		# p = subprocess.call(['subl','parameters.py'],shell=True)#,stdout=subprocess.PIPE)
		# returncode = p.wait()
		# print 'returncode =',returncode
		# p.communicate
		# returncode	= p.wait()
		# subprocess.check_output(['subl','parameters.py'])
		# os.system('parameters.py')
		# while tempfile.NamedTemporaryFile(suffix='task') as temp:
	    # subprocess.call(['subl', 'parameters.py'])
		# access = os.access('veh_map.py',os.W_OK)
		# print 'access =',access
		subprocess.Popen(['subl','-w','parameters.py']).wait()
		pass


		


	def do_reset_config_params(self,line):
		# paramAutoLevelDetection = 'true'
		# paramCpsAdvLevel = 2
		# paramCpsZeroLevel = -2
		# paramDwellStartLevel = 2
		# paramDwellEndLevel = 2
		# paramInjStartLevel = -3#-3    #5
		# paramInjEndLevel = -3#-3   #5
		# paramCdiIgnDetectionLevel = -6
		# paramInjTech = 'carb'	# fi
		# paramCpsType = 'single_pip_tci'
		# paramTotalTeeth = 24
		# paramTotalMissingTeeth = 1
		# parameters.paramInjTech = 'carb'
		# global paramInjTech
		parameters.paramInjTech = 'carb'

	def do_print_temp(self,line):
		# global paramInjTech
		print 'paramInjTech =',parameters.paramInjTech		


	def do_get_avg_outputs(self,line):		
		global gTime,gCps,gIgn,gRpm
		global cpsType
			
		if 0:
			cpsType = raw_input('\nEnter the type of cps and ign (single_pip_tci/single_pip_cdi/dual_pip_tci/dual_pip_cdi/multi_pip_tci/multi_pip_cdi): ')
			if cpsType == 'single_pip_tci' or cpsType == 'dual_pip_tci' or cpsType == 'single_pip_cdi' or cpsType == 'dual_pip_cdi' or cpsType == 'multi_pip_tci' or cpsType == 'multi_pip_cdi':
				print '\nCps type is: ', cpsType ,'\n'
				# print '{}Note: Pls make sure that \n{}1. Pico data is filtered with at least 10kHz. \n2. It is stored in the .mat file.' \
				# '\n3. Ign/Inj angle is calculated from the minimum of zero pulse.\n'.format(Fore.CYAN,Fore.WHITE)

				# sys.exit(1)
			else:
				raise ValueError('Pls enter the valid input')
				sys.exit(1)
		else:
			cpsType = 'single_pip_tci'		
			# cpsType = cps_type
			print '\nCps type is: ', cpsType ,'\n'	
			# print '{}Note: Pls make sure that \n{}1. Pico data is filtered with at least 10kHz. \n2. It is stored in the .mat file.' \
			# '\n3. Ign/Inj angle is calculated from the minimum of zero pulse.\n'.format(Fore.CYAN,Fore.WHITE)
		


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
	# @click.command()
	# @click.option('--entity','-m',click.Choice(['cps','ign','rpm']),multiple=True)
	def do_plot_data(self,line):
		if 0:		# decide whether to plot only cps and ign or rpm also
			# rpm = rpmFromZero
			# print 'gCps_2: \n',gCps
			plt.figure()
			plt.plot(gTime, gCps, gTime, gIgn,  gTime, gRpm)   	# ignAngle
			plt.xlabel('time')
			plt.ylabel('voltage')
			plt.grid()	
		else:
			fig, ax1 = plt.subplots()
			ax2 = ax1.twinx()
			ax1.plot(gTime, gCps, gTime, gIgn)
			# ax2.plot(time,rpmFromAdv, '-r', time,rpmFromZero,'-m')
			# ax2.plot(time,ignAngle,'-r')
			ax2.plot(gTime,gRpm,'-r',label='rpm')	
			ax1.set_xlabel('time')
			ax1.set_ylabel('voltage')	
			ax2.set_ylabel('rpm')	
			plt.grid()
		if 1:		# decide whether to show the plot or save the file. 
			plt.show()
		else:		
			pylab.savefig('\single_pip\\n21_data_3.png')
			pass
		print '\n'
			# return False			

	def help_get_avg_outputs(self):
		print '\nMethod to extract the map from the given input data.\nIt has two arguments 1. cps_type  2. address'
		print 'cps_type = single_pip_tci/dual_pip_tci/single_pip_cdi/dual_pip_cdi'
		print 'address = Address of .mat file generated from pico data.\n'

	# def do_plot_data(self,line):
	# 	print 'Do nothing'

	def postsmd(stop,line):
		print 'Exiting...'
		stop = False


# @click.command()
# # @click.option('--cps_type',prompt= 'Enter the type of cps and ign: ',help = 'single_pip_tci/dual_pip_tci/single_pip_cdi/dual_pip_cdi')
# # @click.option('--cps_type',prompt= 'Enter the type of cps and ign',type = click.Choice(['single_pip_tci','single_pip_cdi','dual_pip_tci','dual_pip_cdi']),help = 'single_pip_tci/dual_pip_tci/single_pip_cdi/dual_pip_cdi')	
# # @click.option('--address',prompt = 'Enter the address of the .mat file: ', help = 'Address of .mat file generated from pico data.')
# @click.option('--cps_type',default = 'none',type = click.Choice(['single_pip_tci','single_pip_cdi','dual_pip_tci','dual_pip_cdi']),help = 'single_pip_tci/dual_pip_tci/single_pip_cdi/dual_pip_cdi')#,prompt= 'Enter the type of cps and ign',type = click.Choice(['single_pip_tci','single_pip_cdi','dual_pip_tci','dual_pip_cdi']),help = 'single_pip_tci/dual_pip_tci/single_pip_cdi/dual_pip_cdi')	
# @click.option('--address',default = 'none', help = 'Address of .mat file generated from pico data.')#,prompt = 'Enter the address of the .mat file: ', help = 'Address of .mat file generated from pico data.')

def cli():	
	#""" Something """
	# print cps_type, '\n', address
	print '{}Note: Pls make sure that \n{}1. Pico data is filtered with at least 10kHz. \n2. It is stored in the .mat file.' \
	'\n3. Ign/Inj angle is calculated from the minimum of zero pulse.\n'.format(Fore.CYAN,Fore.WHITE)

	VehMap().cmdloop()    


if __name__ == '__main__':
    print ''
    # VehMap(cps_type,address).cmdloop()
    cli()
