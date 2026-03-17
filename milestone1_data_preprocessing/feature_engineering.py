import pandas as pd

def create_features(df):

    df["Year"] = df["Date"].dt.year
    df["Month"] = df["Date"].dt.month
    df["Day"] = df["Date"].dt.day
    df["DayOfWeek"] = df["Date"].dt.dayofweek

    print("Feature Engineering Completed")

    print(df[["Date","Year","Month","Day","DayOfWeek"]].head())

    return df
