#Carregar variavel com locais de eventos
from Local_Database import LOCAL_EVENTOS
import os
import h5py
import sys

# Critar metodo que retorna a lista contendo os deslocamentos
def extrair_deslocamentos_arquivo(nome):
    # Carregar arquivo
    dataFile = h5py.File(LOCAL_EVENTOS + nome, 'r')
    # Carregar deslocamentos
    strain = dataFile['strain']['Strain']
    # Carregar tempo
    ts = dataFile['strain']['Strain'].attrs['Xspacing']
    # Carregar meta dados
    meta = dataFile['meta']
    gpsStart = meta['GPSstart'][()]
    duration = meta['Duration'][()]
    gpsEnd = gpsStart + duration
    return [strain, ts, gpsStart, gpsEnd]

if __name__ == '__main__':
    # Lista para armazenar os nomes dos arquivos
    nomes_dos_arquivos = []

    # Percorre todos os arquivos e diretórios no caminho especificado
    for nome_do_arquivo in os.listdir(LOCAL_EVENTOS):
        if os.path.isfile(os.path.join(LOCAL_EVENTOS, nome_do_arquivo)):
            nomes_dos_arquivos.append(nome_do_arquivo)

    # Calcular o menor e maior valor
    final = 1
    maxinfoplot = 15000

    menor = sys.maxsize
    maior = -sys.maxsize - 1

    total = len(nomes_dos_arquivos)
    k = 0
    for i in nomes_dos_arquivos:
        k += 1
        print("Processando arquivo: ", i, " - ", k, " de ", total)
        file = extrair_deslocamentos_arquivo(i)
        strain = file[0][0:maxinfoplot]
        for j in strain:
            if j < menor:
                menor = j
            if j > maior:
                maior = j

    print("Menor valor: ", menor)
    print("Maior valor: ", maior)