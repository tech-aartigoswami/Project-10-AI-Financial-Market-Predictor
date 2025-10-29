import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM

def create_lstm_model(input_shape):
    """Creates and compiles the LSTM model."""
    model = Sequential()
    model.add(LSTM(50, return_sequences=True, input_shape=input_shape))
    model.add(LSTM(50, return_sequences=False))
    model.add(Dense(25))
    model.add(Dense(1))
    model.compile(optimizer='adam', loss='mean_squared_error')
    return model

def train_model(data_df):
    """Prepares data and trains the LSTM model."""
    # We will predict the 'Close' price
    data = data_df.filter(['Close']).values
    
    # Scale the data to be between 0 and 1
    scaler = MinMaxScaler(feature_range=(0,1))
    scaled_data = scaler.fit_transform(data)

    # We will use the past 60 days of data to predict the next day
    prediction_days = 60
    
    X_train = []
    y_train = []

    for i in range(prediction_days, len(scaled_data)):
        X_train.append(scaled_data[i-prediction_days:i, 0])
        y_train.append(scaled_data[i, 0])

    X_train, y_train = np.array(X_train), np.array(y_train)
    X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1], 1))

    # Build and train the model
    model = create_lstm_model((X_train.shape[1], 1))
    print("Training the model... This might take a while.")
    model.fit(X_train, y_train, batch_size=1, epochs=5) # Use more epochs for better accuracy
    print("Model training complete.")

    # You would save the model and scaler to a file to use them for predictions later
    # model.save('stock_predictor.h5')
    
    return model, scaler

# --- Example Usage ---
if __name__ == "__main__":
    from data_fetcher import get_stock_data
    ticker = "RELIANCE.NS"
    data = get_stock_data(ticker, "2020-01-01", "2025-10-28")
    if data is not None:
        trained_model, data_scaler = train_model(data)
