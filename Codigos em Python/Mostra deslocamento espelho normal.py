#Carregar Json com os deslocamentos
import json
import numpy as np
import matplotlib.pyplot as plt

with open('Deslocamentos dos eventos normalizados.json', 'r') as fp:
    data = json.load(fp)

#Escolher deslocamento especifico
name = "H-H1_GWOSC_4KHZ_R1-1126259447-32.hdf5"

#Carregar deslocamento
if name in data:
    deslocamento = data[name][0]
    length = len(data[name][0])
    pos = np.arange(0, length, 1)
    plt.plot(pos, deslocamento)
    plt.show()