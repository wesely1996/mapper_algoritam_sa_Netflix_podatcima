import pandas as pd
import numpy as np
import os

from sklearn.model_selection import train_test_split

if __name__ == '__main__':
    data_dir = "./data"
    # data_file = os.path.join(data_dir, "combined_data_all.csv")
    data_file = os.path.join(data_dir, "combined_data_sample.csv")

    data = pd.read_csv(data_file)
    train_data, test_data = train_test_split(data, test_size=0.2)

    x_train_data = train_data.loc[:, train_data.columns != 'Rating']
    y_train_data = train_data['Rating']

    x_test_data = test_data.loc[:, train_data.columns != 'Rating']
    y_test_data = test_data['Rating']
