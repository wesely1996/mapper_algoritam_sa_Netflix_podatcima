import os
import io
import base64
import argparse

import keras
from keras import backend as K
from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.optimizers import Adam

import kmapper as km
import numpy as np
import pandas as pd

from matplotlib import pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn import metrics, cluster
from sklearn.metrics import classification_report


def fetch_and_transform_data(data_path):
    data = pd.read_csv(data_path)
    data = data.drop(['Date'], axis=1)
    data['MovieID'] = data['MovieID'].astype(int)
    data['CustomerID'] = data['CustomerID'].astype(int)

    return data
    

def create_data_split(data):
    # delimo skup na trening i test
    train_data, test_data = train_test_split(data, test_size=0.2)

    x_train_data = train_data.loc[:, train_data.columns != 'Rating'].values
    y_train_data = train_data['Rating'].values

    x_test_data = test_data.loc[:, train_data.columns != 'Rating'].values
    y_test_data = test_data['Rating'].values

    print('Uci se na ', x_train_data.shape[0], 'primera, a testira se na', x_test_data.shape[0], 'primera')
    
    # ako je ocena 4 ili 5 onda je film preporucen, ako je niza onda nije
    y_train_data = (y_train_data >= 4).astype(int)
    y_test_data = (y_test_data >= 4).astype(int)

    x_train_data = x_train_data.astype(np.float32)
    x_test_data = x_test_data.astype(np.float32)

    return x_train_data, y_train_data, x_test_data, y_test_data


def create_model(hyperparameters):
    model = Sequential()
    model.add(Dense(512, activation='relu', input_shape=(hyperparameters["input_dim"], )))
    model.add(Dropout(0.1))
    model.add(Dense(512, activation='relu'))
    model.add(Dense(hyperparameters["output_dim"], activation='sigmoid'))

    model.summary()
    model.compile(loss='binary_crossentropy',
                  optimizer='adam',
                  metrics=['accuracy'])

    return model


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--data_dir", help="Directory of data", type=str, default="data")
    args, _ = parser.parse_known_args()

    data_path = os.path.join(args.data_dir, "combined_data_sample.csv")
    # data_path = os.path.join(args.data_dir, "combined_data_all.csv")
    data = fetch_and_transform_data(data_path)

    x_train_data, y_train_data, x_test_data, y_test_data = create_data_split(data)

    hyperparameters = {
        "batch_size": 32768,
        "epochs": 1,
        "input_dim": x_train_data.shape[1],
        "output_dim": 1
    }
    model = create_model(hyperparameters)

    history_of_learning = model.fit(x_train_data, y_train_data,
                                    batch_size=hyperparameters["batch_size"],
                                    epochs=hyperparameters["epochs"],
                                    verbose=1,
                                    validation_data=(x_test_data, y_test_data))
    result = model.evaluate(x_test_data, y_test_data, verbose=0)
    print(f'Greska: {result[0]}')
    print(f'Tacnost: {result[1]}')

    y_test_preds = model.predict(x_test_data, batch_size=hyperparameters["batch_size"]).flatten()
    y_test_preds = np.where(y_test_preds > 0.5, 1, 0).astype(np.int32)
    print(classification_report(y_test_data, y_test_preds))

    # number_of_passes = 1000
    # predicted_stochastic = K.function(inputs=[model.layers[0].input, K.learning_phase()],
    #                                   outputs=[model.layers[-1].output])

    # y_pred_test = np.array([predicted_stochastic([x_test_data, 1]) for _ in range(number_of_passes)])
    # y_pred_stochs_test = y_pred_test.reshape(-1, y_test_data.shape[0]).T

    # y_pred_std_test = np.std(y_pred_stochs_test, axis=1)
    # y_pred_mean_test = np.mean(y_pred_stochs_test, axis=1)
    # y_pred_modus_test = (np.mean(y_pred_stochs_test > .5, axis=1) > .5).astype(int).reshape(-1, 1)

    # y_pred_var_rel_test = 1 - np.mean((y_pred_stochs_test > .5) == y_pred_modus_test, axis=1)

    # analyse_test_results = pd.DataFrame({
    #     "y_tacno": y_test_data,
    #     "y_pred": y_pred_mean_test,
    #     "VR": y_pred_var_rel_test,
    #     "STD": y_pred_std_test
    # })

    # print("Tacnost:", metrics.accuracy_score(y_true=y_test_data, y_pred=y_pred_mean_test > .5))
    # print("Opis rezultata:")
    # print(analyse_test_results.describe())

