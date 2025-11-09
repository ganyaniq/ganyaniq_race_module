# ganyaniq_race_module/utils/data_processor.py

import pandas as pd

def normalize_columns(df):
    df.columns = [col.lower().replace(" ", "_") for col in df.columns]
    return df

def fill_missing_values(df):
    for col in df.select_dtypes(include=['float64', 'int64']).columns:
        df[col].fillna(df[col].mean(), inplace=True)
    return df

def encode_categorical(df):
    categorical_cols = df.select_dtypes(include=['object']).columns
    return pd.get_dummies(df, columns=categorical_cols)

def prepare_for_model(df):
    df = normalize_columns(df)
    df = fill_missing_values(df)
    df = encode_categorical(df)
    return df
