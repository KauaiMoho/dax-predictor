import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from keras.models import Sequential
from keras.layers import LSTM, Bidirectional, Dense, Dropout

model = Sequential()

# Add a bidirectional LSTM layer
model.add(Bidirectional(LSTM(64, return_sequences=True), input_shape=(X_train.shape[1], X_train.shape[2]))) # FIX SHAPE
model.add(Dropout(0.2))  # Regularization to prevent overfitting

# Add another LSTM layer
model.add(Bidirectional(LSTM(32)))
model.add(Dropout(0.2))

# Fully connected layer for output
model.add(Dense(1))

model.compile(optimizer='adam', loss='mean_squared_error')
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

#Sequence data for BiLSTM - CHECK
def create_sequences(data, seq_length=30):
    sequences = []
    for i in range(len(data) - seq_length):
        seq = data.iloc[i:i+seq_length]
        sequences.append(seq.values)
    return np.array(sequences)

sequences = create_sequences(averaged)
print(sequences)