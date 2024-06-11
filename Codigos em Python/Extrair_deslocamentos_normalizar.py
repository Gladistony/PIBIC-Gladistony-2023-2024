#Carregar variavel com locais de eventos
from Local_Database import LOCAL_EVENTOS
from Local_Database import MENOR_VALOR
from Local_Database import MAIOR_VALOR
from Extrair_deslocamentos_min_max import extrair_deslocamentos_arquivo
import os
import numpy as np
import json

def normalizar_dados(dados):
    nparray = np.array(dados)
    base = 1e-12
    dados = nparray / base
    dados = dados + 0.5
    return dados
    #return (nparray - MENOR_VALOR) / (MAIOR_VALOR - MENOR_VALOR)

if __name__ == '__main__':
    # Lista para armazenar os nomes dos arquivos
    nomes_dos_arquivos = []

    # Percorre todos os arquivos e diretórios no caminho especificado
    for nome_do_arquivo in os.listdir(LOCAL_EVENTOS):
        if os.path.isfile(os.path.join(LOCAL_EVENTOS, nome_do_arquivo)):
            nomes_dos_arquivos.append(nome_do_arquivo)

    final = 15000
    #Criar dataframe com a coluna do nome, dados normalizados
    dataframe = {}
    tamanho = len(nomes_dos_arquivos)
    k = 0
    for file in nomes_dos_arquivos:
        k += 1
        print("Processando arquivo: ", file, " - ", k, " de ", tamanho)
        lido = extrair_deslocamentos_arquivo(file)[0]
        normal = normalizar_dados(lido[0:final])
        #normal = np.round(normal, 5)
        dataframe[file] = [normal.tolist(), lido[1], lido[2], lido[3]]
    
    #salvar dataframe como json
    with open('Deslocamentos dos eventos normalizados.json', 'w') as fp:
        json.dump(dataframe, fp)
