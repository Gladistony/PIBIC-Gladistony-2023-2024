import os
import re
import gwosc
import gwpy
from gwpy.timeseries import TimeSeries
from scipy.signal import get_window
import matplotlib.pyplot as plt

DATA = "C:/Lista de Evenntos/Gerar Graficos/"

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
print("Salvar dados de deslocamento do interferômetro em grafico")
for evento, observatorios in Lista_eventos.items():
    data = {}
    for observatorio in observatorios:
        try:
            data[observatorio] = TimeSeries.read(f"{DATA}{observatorio}-{evento}.hdf5")
        except Exception as e:
            print(f"Não foi possível ler o arquivo {observatorio}-{evento}.hdf5: {e}")
    plt.figure(figsize=(10, 5))
    for observatorio in observatorios:
        plt.plot(data[observatorio], label=observatorio)
    plt.title(f"Deslocamento do interferômetro para o evento {evento}")
    plt.savefig(f"{DATA}{evento} deslocamento bruto.png")
print("Aplicar FFT nos dados de deslocamento do interferômetro")
for evento, observatorios in Lista_eventos.items():
    fft = {}
    for observatorio in observatorios:
        try:
            processo = TimeSeries.read(f"{DATA}{observatorio}-{evento}.hdf5").fft().abs()
            fft[observatorio] = processo
        except Exception as e:
            print(f"Não foi possível aplicar fft nos dados {observatorio}-{evento}: {e}")
    plt.figure(figsize=(10, 5))
    for observatorio in observatorios:
        plt.plot(fft[observatorio], label=observatorio)
    plt.title(f"FFT dos dados de deslocamento do interferômetro para o evento {evento}")
    plt.savefig(f"{DATA}{evento} fft.png")
print("Aplicar janela nos dados de deslocamento do interferômetro")
for evento, observatorios in Lista_eventos.items():
    janela = {}
    for observatorio in observatorios:
        try:
            processo = TimeSeries.read(f"{DATA}{observatorio}-{evento}.hdf5")
            janela[observatorio] = processo * get_window("hann", len(processo))
        except Exception as e:
            print(f"Não foi possível aplicar janela nos dados {observatorio}-{evento}: {e}")
    plt.figure(figsize=(10, 5))
    for observatorio in observatorios:
        plt.plot(janela[observatorio], label=observatorio)
    plt.title(f"Janela aplicada nos dados de deslocamento do interferômetro para o evento {evento}")
    plt.savefig(f"{DATA}{evento} janela.png")
print("Definindo cores usadas")
cores = {}
cores['G1'] = 'blue'
cores['H1'] = 'gwpy:ligo-hanford'
cores['L1'] = 'gwpy:ligo-livingston'
cores['V1'] = 'green'
cores['K1'] = 'gwpy:ligo-kil'
print("Aplicar asd nos dados e criar graficos finais")
for evento, observatorios in Lista_eventos.items():
    asd = {}
    for observatorio in observatorios:
        try:
            processo = TimeSeries.read(f"{DATA}{observatorio}-{evento}.hdf5")
            asd[observatorio] = processo.asd(fftlength=4, method="median")
        except Exception as e:
            print(f"Não foi possível aplicar asd nos dados {observatorio}-{evento}: {e}")
    plt.figure(figsize=(10, 5))
    for observatorio in observatorios:
        plt.loglog(asd[observatorio], label=observatorio, color=cores[observatorio])
    plt.title(f"ASD dos dados de deslocamento do interferômetro para o evento {evento}")
    plt.savefig(f"{DATA}{evento} asd.png")