import pandas as pd
import numpy as np
import os

LOCALXLSXTREINO = "c:/Lista de Evenntos/xlsx/"

def carregar_dados_xlsx(arquivo, coluna="Pontos"):
    df = pd.read_excel(arquivo)
    return df[coluna]

def listar_arquivos_com_extensao(pasta, extensao):
    arquivos = [f for f in os.listdir(pasta) if f.endswith(extensao)]
    return arquivos

arq = listar_arquivos_com_extensao(LOCALXLSXTREINO, ".xlsx")

#Criar um novo dataframe com 200 colunas de a0001 até a0200 e outra coluna com resultado
datafinal = pd.DataFrame(columns=[f"a{str(i).zfill(4)}" for i in range(1, 201)] + ["Resultado"])

for arquivo in arq:
    dados = carregar_dados_xlsx(f"{LOCALXLSXTREINO}{arquivo}")
    #Transformar dados numa lista
    dados = dados.tolist()
    dados = np.array(dados)
    #Selecionar 200 pontos desses dados uniformemente e adicionar a um novo dataframe
    indices = np.linspace(0, len(dados) - 1, 200, dtype=int)
    selected_elements = dados[indices]
    resultado = carregar_dados_xlsx(f"{LOCALXLSXTREINO}{arquivo}", "Resultado")
    datafinal.loc[len(datafinal)] = selected_elements + [resultado[0]]

datafinal.to_excel("c:/Lista de Evenntos/xlsx/resultado.xlsx", index=False)
