#import packages
import io
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pylab import rcParams
from sklearn.preprocessing import MinMaxScaler
import os
from flask import send_file

def upload(name, url):
    import requests


df = ''
df_unprocessed = ''

def read_file(arg1):
    rcParams['figure.figsize'] = 20,10


    global df
    global df_unprocessed
    #read the file
    try:
        APP_ROOT = os.path.dirname(os.path.abspath(__file__))
        filename = APP_ROOT+'/'+arg1+'.csv'
        print(filename)
        df_unprocessed = pd.read_csv(filename)
        df = df_unprocessed.iloc[:, 1:2].values
        return "File ready"
    except Exception as e:
        return "File not Found - " + str(e)


def plot_data():
    #TODO
    global df
    if df == '': return "Read a file in /read_file"
    plt.figure(figsize=(16,8))
    plt.plot(df, label='Close Price history')
    bytes_image = io.BytesIO()
    plt.savefig(bytes_image, format='png')
    bytes_image.seek(0)
    return bytes_image

def plot_data2():
    bytes_obj = plot_data()
    return send_file(bytes_obj, attachment_filename='plot.png', mimetype='image/png') 

def split_data():
    global df
    if df == '': return "Read a file in /read_file"

    scaler = MinMaxScaler(feature_range = (0, 1))

    scaled = scaler.fit_transform(df)
    features_set = []
    labels = []

    train_size = int(0.8*len(df))
    test = df[train_size:]

    for i in range(60, train_size):
        features_set.append(scaled[i-60:i, 0])
        labels.append(scaled[i, 0])
        
    features_set, labels = np.array(features_set), np.array(labels)
    features_set = np.reshape(features_set, (features_set.shape[0], features_set.shape[1], 1))
    return "Spliting of data done"



def train_model():
    #importing required libraries
    from sklearn.preprocessing import MinMaxScaler
    from keras.models import Sequential, load_model
    from keras.layers import Dense, Dropout, LSTM
    split_data()

    model = Sequential()
    model.add(LSTM(units=50, return_sequences=True, input_shape=(features_set.shape[1], 1)))
    model.add(Dropout(0.2))
    model.add(LSTM(units=50, return_sequences=True))
    model.add(Dropout(0.2))

    model.add(LSTM(units=50, return_sequences=True))
    model.add(Dropout(0.2))

    model.add(LSTM(units=50))
    model.add(Dropout(0.2))
    model.add(Dense(1))

    model.compile(loss='mean_squared_error', optimizer='adam')
    model.fit(features_set, labels, epochs = 31, batch_size = 32)

    #save the model so that I dont need to run it again
    model.save('lstm_model.h5')
    return "Model trained"


def predict():
    global predictions
    global apple_testing_processed
    #load model from the file
    from keras.models import Sequential, load_model
    split_data()
    model = load_model('lstm_model.h5')

    train_size = int(0.8*len(df))
    test = df[train_size:]
    scaler = MinMaxScaler(feature_range = (0, 1))
    scaled = scaler.fit_transform(df)
    features_set = []
    apple_testing_processed = test
    test_inputs = df_unprocessed['Open'][train_size - 60:].values
    test_inputs = test_inputs.reshape(-1,1)
    test_inputs = scaler.transform(test_inputs)

    test_features = []
    for i in range(60, len(test_inputs)):
        test_features.append(test_inputs[i-60:i, 0])
    test_features = np.array(test_features)
    test_features = np.reshape(test_features, (test_features.shape[0], test_features.shape[1], 1))

    predictions = model.predict(test_features)
    predictions = scaler.inverse_transform(predictions)
    return "Predictions made"


def plot_predictions1():
    #plot the predictions
    plt.figure(figsize=(10,6))
    plt.plot(apple_testing_processed, color='blue', label='Actual Apple Stock Price')
    plt.plot(predictions , color='red', label='Predicted Apple Stock Price')
    plt.title('Apple Stock Price Prediction')
    plt.xlabel('Date')
    plt.ylabel('Apple Stock Price')
    bytes_image = io.BytesIO()
    plt.savefig(bytes_image, format='png')
    bytes_image.seek(0)
    return bytes_image

def plot_predictions():
    bytes_obj = plot_predictions1()
    return send_file(bytes_obj, attachment_filename='plot.png', mimetype='image/png') 
