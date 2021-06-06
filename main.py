import argparse
from collections import deque
import os

import numpy as np
import pandas as pd
from sklearn.neighbors import KNeighborsTransformer


def load_and_refine_data(data_path):
    df_raw = pd.read_csv(data_path, header=None, names=["User", "Rating", "Date"], usecols=[0, 1, 2])

    tmp_movies = df_raw[df_raw["Rating"].isna()]["User"].reset_index()
    movie_indices = [[index, int(movie[:-1])] for index, movie in tmp_movies.values]

    shifted_movie_indices = deque(movie_indices)
    shifted_movie_indices.rotate(-1)

    user_data = []
    for [df_id_1, movie_id], [df_id_2, next_movie_id] in zip(movie_indices, shifted_movie_indices):
        if df_id_1<df_id_2:
            tmp_df = df_raw.loc[df_id_1+1:df_id_2-1].copy()
        else:
            tmp_df = df_raw.loc[df_id_1+1:].copy()
            
        tmp_df["Movie"] = movie_id
        user_data.append(tmp_df)

    df = pd.concat(user_data)
    del user_data, df_raw, tmp_movies, tmp_df, shifted_movie_indices, movie_indices
    del df_id_1, movie_id, df_id_2, next_movie_id
    print(f"Shape of raw User-Ratings: {df.shape}")

    return df


def filter_data(df):
    min_movie_ratings = 10000
    filter_movies = (df["Movie"].value_counts() > min_movie_ratings)
    filter_movies = filter_movies[filter_movies].index.tolist()

    min_user_ratings = 200
    filter_users = (df["User"].value_counts() > min_user_ratings)
    filter_users = filter_users[filter_users].index.tolist()

    df_filterd = df[(df['Movie'].isin(filter_movies)) & (df['User'].isin(filter_users))]
    del filter_movies, filter_users, min_movie_ratings, min_user_ratings
    print(f"Shape of filtered User-Ratings: {df_filterd.shape}")

    return df_filterd


def create_train_test_split(df_filtered, n=100000):
    df_filtered = df_filtered.drop('Date', axis=1).sample(frac=1).reset_index(drop=True)

    # Split train- & testset
    df_train = df_filtered[:-n]
    df_test = df_filtered[-n:]

    return df_train, df_test


def make_data_sparse(df):
    df_p = df.pivot_table(index="User", columns="Movie", values="Rating", fill_value=0)
    print(f"Shape of User-Movie: {df_p.shape}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--data_dir", type=str, default="./data")
    args, _ = parser.parse_known_args()

    data_path = os.path.join(args.data_dir, "combined_data_1.txt")
    df_raw = load_and_refine_data(data_path)
    df_filtered = filter_data(df_raw)
    df_train, df_test = create_train_test_split(df_filtered)

    df_train_sparse = make_data_sparse(df_train)
    df_test_sparse = make_data_sparse(df_test)

    # model = KNeighborsTransformer(n_neighbors=5)
    # model.fit(df_train_sparse)