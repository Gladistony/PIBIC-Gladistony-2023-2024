import h5py
import numpy as np
import matplotlib.pyplot as plt

#Carregar variavel com locais de eventos
from Local_Database import LOCAL_EVENTOS

def dump_info(name, obj):
    print ("{0} :".format(name))
    try:
        print ("   .value: {0}".format(obj.value))
        for key in obj.attrs.keys():
            print("     .attrs[{0}]:  {1}".format(key, obj.attrs[key]))
    except:
	    pass

filename = LOCAL_EVENTOS + '/H-H1_GWOSC_4KHZ_R1-1126259447-32.hdf5'
dataFile = h5py.File(filename, 'r')
for keys in dataFile.keys():
    print (keys)

#---------------------
# Read in strain data
#---------------------
strain = dataFile['strain']['Strain']
ts = dataFile['strain']['Strain'].attrs['Xspacing']
print("Tempo",ts)
#-----------------------
# Print out some meta data
#-----------------------
print("\n\n")
metaKeys = dataFile['meta'].keys()
meta = dataFile['meta']
for key in metaKeys:
    print (key, meta[key][()])
print("Type of strain data: {0}".format(type(strain)))
#---------------------------
# Create a time vector
#---------------------------
gpsStart = meta['GPSstart'][()]#.value
duration = meta['Duration'][()]
gpsEnd   = gpsStart + duration

time = np.arange(gpsStart, gpsEnd, ts)

#----------------------
# Plot the time series
#----------------------
numSamples = 15000
plt.plot(time[0:numSamples], strain[0:numSamples])
plt.xlabel('GPS Time (s)')
plt.ylabel('H1 Strain')
plt.show()