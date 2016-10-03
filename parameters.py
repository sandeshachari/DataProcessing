# Configurable parameters: start

# paramAutoLevelDetection = 'true'
# paramCpsAdvLevel = 4
# paramCpsZeroLevel = -4
# paramDwellStartLevel = 4
# paramDwellEndLevel = 4
# paramInjStartLevel = 3		#-3    #5
# paramInjEndLevel = 3		#-3    #5
# paramCdiIgnDetectionLevel = -6
# paramInjTech = 'fi'	   # carb 	#fi
# paramCpsType = 'single_pip_tci'  # single_pip_tci	single_pip_cdi	dual_pip_tci	dual_pip_cdi	multi_pip_tci	multi_pip_cdi
# paramTotalTeeth = 15
# paramTotalMissingTeeth = 3
# paramCpsChannel = 'A'
# paramIgnChannel = 'B'
# paramInjChannel = 'C'

# global params
params = []

cpsType = 'single_pip_tci'
cpsAdvLevel = 4
cpsZeroLevel = -4

dwellStartLevel = 4
dwellEndLevel = -4
cdiIgnDetectionLevel = -6

injStartLevel = 3
injEndLevel = 3

injTech = 'fi'
autoLevelDetection = True

nTeeth = 12
nMissingTeeth = 3

# Pico channels setting
cpsChannel = 'A'
ignChannel = 'B'
injChannel = 'C'

numLines = sum(1 for line in open('set_params.txt'))

f = open(r'set_params.txt','r');
filedata = f.read()

f.seek(0)

for i in range(0,numLines):
	params.append(str.split(f.readline())[0])

f.close()




# Configurable parameters: end
