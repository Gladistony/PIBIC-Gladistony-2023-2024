import os
import re
import gwosc
import gwpy
from gwpy.timeseries import TimeSeries
from pycbc.types import TimeSeries as PyCBCtimeSeries
from pycbc.filter import resample_to_delta_t, highpass
from pycbc.psd import interpolate, inverse_spectrum_truncation
from pycbc.waveform import get_td_waveform
from gwosc.datasets import event_gps
import pandas as pd

DATA = "C:/Lista de Evenntos/"

def listar_arquivos_com_extensao(pasta, extensao):
    arquivos = [f for f in os.listdir(pasta) if f.endswith(extensao)]
    return arquivos

arq = listar_arquivos_com_extensao(DATA, ".hdf5")
padrao = r"(?P<observatorio>[^-]+)-(?P<nome_arquivo>[^.]+)\.hdf5"
print(f"Lista total de arquivos com extensão .hdf5: {len(arq)}")
Lista_eventos = {}
for arquivo in arq:
    resultado = re.match(padrao, arquivo)
    if resultado:
        observatorio = resultado.group("observatorio")
        nome_arquivo = resultado.group("nome_arquivo")
        if nome_arquivo not in Lista_eventos:
            Lista_eventos[nome_arquivo] = []
        Lista_eventos[nome_arquivo].append(observatorio)
print("Ajustando dados de baixa frequencia ")
dataStrain = {}
conditioneds = {}
psds = {}
for evento, observatorios in Lista_eventos.items():
    for obs in observatorios:
        data = TimeSeries.read(f"{DATA}{obs}-{evento}.hdf5")
        #Converter TimeSeries
        ddata = data.data
        ddelta = data.dt.value
        epoch = data.t0.value
        tserie = PyCBCtimeSeries(ddata, delta_t=ddelta, epoch=epoch)
        strain = highpass(data, 15.0)
        strain = resample_to_delta_t(strain, 1.0/2048)
        if evento not in dataStrain:
            dataStrain[evento] = {}
            conditioneds[evento] = {}
            psds[evento] = {}
        dataStrain[evento][obs] = strain
        conditioned = strain.crop(2, 2)
        conditioneds[evento][obs] = conditioned
        psd = conditioned.psd(4)
        psd = interpolate(psd, conditioned.delta_f)
        inverse_spectrum_truncation(psd, int(4 * conditioned.sample_rate),
                                  low_frequency_cutoff=15)
        psds[evento][obs] = psd
        white_data = (conditioned.to_frequencyseries() / psd**0.5).to_timeseries()
        white_data = white_data.highpass_fir(30., 512).lowpass_fir(300, 512)
        merger = event_gps(evento).value
        white_data = white_data.time_slice(merger-.2, merger+.1)
        pontos = white_data.numpy()
        tempos = white_data.sample_times
        dados = pd.DataFrame({"Tempo": tempos, "Pontos": pontos})
        dados.to_excel(f"excel/{DATA}{obs}-{evento}.xlsx")