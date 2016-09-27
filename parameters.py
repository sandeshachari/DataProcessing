# Configurable parameters: start

paramAutoLevelDetection = 'true'
paramCpsAdvLevel = 4
paramCpsZeroLevel = -4
paramDwellStartLevel = 4
paramDwellEndLevel = 4
paramInjStartLevel = 3		#-3    #5
paramInjEndLevel = 3		#-3    #5
paramCdiIgnDetectionLevel = -6

# global paramInjTech
paramInjTech = 'fi'	   # carb 	#fi
paramCpsType = 'single_pip_tci'  # single_pip_tci	single_pip_cdi	dual_pip_tci	dual_pip_cdi	multi_pip_tci	multi_pip_cdi

paramTotalTeeth = 12
paramTotalMissingTeeth = 3


cpsType = paramCpsType
cpsAdvLevel = paramCpsAdvLevel
cpsZeroLevel = paramCpsZeroLevel

dwellStartLevel = paramDwellStartLevel
dwellEndLevel = paramDwellEndLevel
cdiIgnDetectionLevel = paramCdiIgnDetectionLevel

injStartLevel = paramInjStartLevel
injEndLevel = paramInjEndLevel

nTeeth = paramTotalTeeth
nMissingTeeth = paramTotalMissingTeeth


def init():
	paramAutoLevelDetection = 'true'
	paramCpsAdvLevel = 2
	paramCpsZeroLevel = -2
	paramDwellStartLevel = 2
	paramDwellEndLevel = 2
	paramInjStartLevel = -3		#-3    #5
	paramInjEndLevel = -3		#-3    #5
	paramCdiIgnDetectionLevel = -6

	# global paramInjTech
	paramInjTech = 'fi'	   # carb 	#fi
	paramCpsType = 'single_pip_tci'  # single_pip_tci	single_pip_cdi	dual_pip_tci	dual_pip_cdi	multi_pip_tci	multi_pip_cdi

	paramTotalTeeth = 24
	paramTotalMissingTeeth = 1

# Configurable parameters: end
