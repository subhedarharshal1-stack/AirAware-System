from feature_engineering import create_features
import pandas as pd

def load_data(path):
    df = pd.read_csv(path)
    print("Dataset Loaded")
    print(df.head())
    return df


def clean_data(df):
    df["Date"] = pd.to_datetime(df["Date"])
    df = df.fillna(df.mean(numeric_only=True))
    df = df.dropna()

    print("Data Cleaned")

    return df


if __name__ == "__main__":
    df = load_data("data/air_quality.csv")
    df = clean_data(df)
    df = create_features(df)
    print("Cleaned Data Preview:")
    print(df.head())
