from pycbc.waveform import get_td_waveform 
import pandas as pd
import random
import numpy as np

numero_ondas = 60
verdadeira = True

if verdadeira:
    m1 = random.randrange(10, 100)
    m2 = random.randrange(10, 100)
    hp, hc = get_td_waveform(approximant="SEOBNRv4_opt",
                             mass1=m1,
                             mass2=m2,
                             delta_t=1.0/2048,
                             f_lower=20)
    dados = hp.numpy()
    #Adicionar ruido
    np.random.seed(0)
    sigma = 0.25
    dados += np.random.normal(0, sigma, len(dados))
    tempos = hp.sample_times
    df = pd.DataFrame({"Tempo": tempos, "Pontos": dados})
    df.to_excel("Ondas Verdadeiras/ondas.xlsx", index=False)
else:
    x = np.linspace(0, 10, 1000)
    y = np.sin(2 * np.pi * x) + np.random.normal(0, 0.1, x.shape)
    df = pd.DataFrame({"Tempo": x, "Pontos": y})
    df.to_excel("Ondas Falsas/ondas.xlsx", index=False)
