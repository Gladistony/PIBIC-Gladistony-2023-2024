import pandas as pd
import numpy as np
import glob
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from keras.models import Sequential
from keras.layers import LSTM, Dense
from sklearn.metrics import confusion_matrix


file_paths = glob.glob('c:/Lista de Evenntos/xlsx/resultado.xlsx')
data_list = []

for file_path in file_paths:
    df = pd.read_excel(file_path)
    data_list.append(df)

combined_data = pd.concat(data_list)

# Pré-processamento
X = combined_data.drop(columns=["Resultado"]).values
y = combined_data["Resultado"].values

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# Modelo Simples (Regressão Logística)
model = LogisticRegression()
model.fit(X_train, y_train)
y_pred = model.predict(X_test)
print(f'Acurácia da Regressão Logística: {accuracy_score(y_test, y_pred)}')

# Modelo Complexo (LSTM)
X_train = X_train.reshape((X_train.shape[0], 1, X_train.shape[1]))
X_test = X_test.reshape((X_test.shape[0], 1, X_test.shape[1]))

lstm_model = Sequential()
lstm_model.add(LSTM(50, activation='relu', input_shape=(1, X_train.shape[2])))
lstm_model.add(Dense(1, activation='sigmoid'))
lstm_model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

lstm_model.fit(X_train, y_train, epochs=200, batch_size=32, verbose=0)
loss, accuracy = lstm_model.evaluate(X_test, y_test, verbose=0)
print(f'Acurácia do LSTM: {accuracy}')

y_pred = (lstm_model.predict(X_test) > 0.5).astype("int32")
# Calcular a matriz de confusão
tn, fp, fn, tp = confusion_matrix(y_test, y_pred).ravel()

print(f'Verdadeiros Positivos (TP): {tp}')
print(f'Verdadeiros Negativos (TN): {tn}')
print(f'Falsos Positivos (FP): {fp}')
print(f'Falsos Negativos (FN): {fn}')