import pandas as pd
import numpy as np
import os
import base64

# Tensorflow only supports Python 3.5 to 3.8. => change python interpreter to 3.8
# import keras
# from keras import backend as K
# from keras.models import Sequential
# from keras.layers import Dense, Dropout
# from keras.optimizers import Adam

from sklearn.model_selection import train_test_split

if __name__ == '__main__':
    data_dir = "./data"
    # data_file = os.path.join(data_dir, "combined_data_all.csv")
    data_file = os.path.join(data_dir, "combined_data_sample.csv")

    # ucitavamo bazu podataka i transformisemo podatke u odgovarajuce tipove
    data = pd.read_csv(data_file)
    data['MovieID'] = data['MovieID'].astype(int)
    data['CustomerID'] = data['CustomerID'].astype(int)
    data['Date'] = pd.to_datetime(data['Date'], format='%Y-%m-%d')

    # delimo skup na trening i test
    train_data, test_data = train_test_split(data, test_size=0.2)

    x_train_data = train_data.loc[:, train_data.columns != 'Rating']
    y_train_data = train_data['Rating']

    x_test_data = test_data.loc[:, train_data.columns != 'Rating']
    y_test_data = test_data['Rating']

    print('Uci se na ', x_train_data.shape[0], ' primera, a testira se na ', x_test_data.shape[0], ' primera')

    # ako je ocena 4 ili 5 onda je film preporucen, ako je niza onda nije
    y_train_data = (y_train_data >= 4).astype(int)
    y_test_data = (y_test_data >= 4).astype(int)

    # Model
    heep_size = 128
    class_number = 1
    epoch_number = 10

    # model = Sequential()