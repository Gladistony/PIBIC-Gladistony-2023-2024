import gwosc
import gwpy
from gwosc.datasets import find_datasets
from gwpy.timeseries import TimeSeries
from gwosc.datasets import event_gps
catalogos = find_datasets(type="catalog")
print(f"Lista de catalogos {catalogos}")
eventos = gwosc.datasets.find_datasets(type="events")
print(f"Lista de eventos {eventos}")
ultima_versao = {}
for dataset in eventos:
    if "gw" in dataset.lower():
      event_name = dataset.split('-')[0]
      if event_name not in ultima_versao or dataset > ultima_versao[event_name]:
          ultima_versao[event_name] = dataset
ultima_versao = list(ultima_versao.values())
print(f"Lista de versiones de eventos {ultima_versao}")
print(f"Total de eventos {len(ultima_versao)}")
temposGPS = []
for version in ultima_versao:
    events = event_gps(version)
    temposGPS.append(events)
print(f"Lista de segmentos {temposGPS}")
OBSERV = ['G1', 'H1', 'L1', 'V1', 'K1']
ldata = []
segmentos = []
intervalo = 512
for gps in temposGPS:
    segment = (int(gps)-intervalo, int(gps)+intervalo)
    segmentos.append(segment)
id = 0
for segmento in segmentos:
    dado = {}
    for obs in OBSERV:
        try:
            data = TimeSeries.fetch_open_data(obs, *segmento, verbose=True, cache=True)
            dado[obs] = data
        except Exception as e:
            print(f"Não foi possível obter dados para {obs} no segmento {segmento}: {e}")
    ldata.append(dado)
    data.write(f"data/{obs}-{ultima_versao[id]}.hdf5", "hdf5")
    id += 1