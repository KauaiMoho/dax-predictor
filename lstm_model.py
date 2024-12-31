import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from keras.models import Sequential
from keras.layers import LSTM, Bidirectional, Dense, Dropout

from tensorflow.python.client import device_lib
print(device_lib.list_local_devices())

sentiment = pd.read_csv('sentiments_merged.csv', parse_dates=["date"])
data = pd.read_csv('dax_2019-2024.csv', parse_dates=["Date"])
data.rename(columns={"Date": "date"}, inplace=True)

df = pd.merge(data, sentiment, on='date')
df.drop(['Change %', 'title'], axis=1, inplace=True)

df["Price"] = df["Price"].str.replace(",", "").astype(float)
df["Open"] = df["Open"].str.replace(",", "").astype(float)
df["High"] = df["High"].str.replace(",", "").astype(float)
df["Low"] = df["Low"].str.replace(",", "").astype(float)
df["Vol."] = df["Vol."].str.replace(",", "").str.replace("M", "").astype(float)*1000000

#Normalization using Z-score
scaler = StandardScaler()
numeric_columns = ['Price', 'Open', 'High', 'Low', "Vol."]
df[numeric_columns] = scaler.fit_transform(df[numeric_columns])

#Averaging of repeated sentiments
averaged = df.groupby('date').mean()
print(averaged)

#Sequence data for BiLSTM
def create_sequences(data, lookback, forecast_horizon):
    X, y = [], []
    for i in range(len(data) - lookback - forecast_horizon + 1):
        X.append(data.iloc[i:i+lookback].values)
        y.append(data.iloc[i+lookback:i+lookback+forecast_horizon]['Price'].values) 
    return np.array(X), np.array(y)

lookback = 60
forecast_horizon = 30  
X, y = create_sequences(averaged, lookback, forecast_horizon)

train_size = int(0.8 * len(X))
X_train, X_test = X[:train_size], X[train_size:]
y_train, y_test = y[:train_size], y[train_size:]

#Create BiLSTM
model = Sequential([
    Bidirectional(LSTM(128, return_sequences=True), input_shape=(lookback, X.shape[2])),
    Dropout(0.2),
    Bidirectional(LSTM(64)),
    Dropout(0.2),
    Dense(forecast_horizon)
])

model.compile(optimizer='adam', loss='mean_squared_error')

#Train
history = model.fit(
    X_train, y_train,
    epochs=20,
    batch_size=32,
    validation_split=0.2
)

#Test
loss = model.evaluate(X_test, y_test)
print("Test Loss:", loss)