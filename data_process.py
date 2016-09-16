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



class DataProcess():

	def __init__(self,time,cps,ign):
		self.time = time
		self.cps = cps
		self.ign = ign

	def extractInfo():
		


