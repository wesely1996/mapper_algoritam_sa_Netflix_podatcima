import os
import io
import base64

import keras
from keras import backend as k
from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.optimizers import Adam

import kmapper as km
import numpy as np
import pandas as pd

from matplotlib import pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn import metrics, cluster

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
    heep_size = int(len(x_train_data.index) / 100)
    class_number = 1
    epoch_number = 10

    model = Sequential()
    model.add(Dropout(0.5, input_shape=(3,)))
    model.add(Dense(512, activation='relu', input_shape=(3,)))
    model.add(Dropout(0.5))
    model.add(Dense(512, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(class_number, activation='sigmoid'))

    model.summary()
    model.compile(loss='binary_crossentropy',
                  optimizer=Adam(),
                  metrics=['accuracy'])

    history_of_learning = model.fix(x_train_data, y_train_data,
                                    batch_size=heep_size,
                                    epochs=epoch_number,
                                    verbose=1,
                                    validation_data=(x_test_data, y_test_data))
    result = model.evaluate(x_test_data, y_test_data, verbose=0)
    print("Greska: ", result[0], "\nTacnost: ", result[1])

    number_of_passes = 1000

    predicted_stochs = k.function(input=[model.layers[0].input,
                                              k.learning_phase()],
                                       output=[model.layers[-1].output])

    y_pred_test = np.array([predicted_stochs([x_test_data, 1]) for _ in range(number_of_passes)])
    y_pred_stochs_test = y_pred_test.reshape(-1, y_test_data.shape[0]).T

    y_pred_std_test = np.std(y_pred_stochs_test, axis=1)
    y_pred_mean_test = np.mean(y_pred_stochs_test, axis=1)
    y_pred_modus_test = (np.mean(y_pred_stochs_test > .5, axis=1) > .5).astype(int).reshape(-1, 1)

    y_pred_var_rel_test = 1 - np.mean((y_pred_stochs_test > .5) == y_pred_modus_test, axis=1)

    analyse_test_results = pd.DataFrame({
        "y_tacno": y_test_data,
        "y_pred": y_pred_mean_test,
        "VR": y_pred_var_rel_test,
        "STD": y_pred_std_test
    })

    print("Tacnost:", metrics.accuracy_score(y_true=y_test_data, y_pred=y_pred_mean_test > .5))
    print("Opis rezultata:")
    print(analyse_test_results.describe())

