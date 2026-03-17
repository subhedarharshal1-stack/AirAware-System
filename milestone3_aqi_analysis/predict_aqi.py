import pandas as pd
import joblib
from aqi_category import get_aqi_category
from alert_system import generate_alert

# Load trained model
model = joblib.load("milestone2_forecasting_model/aqi_model.pkl")

# Load dataset
df = pd.read_csv("data/air_quality.csv")

# Remove rows without AQI
df = df.dropna(subset=["AQI"])

# Use numeric columns only
df_numeric = df.select_dtypes(include=["number"])

# Features (drop AQI)
X = df_numeric.drop("AQI", axis=1)

# Take first sample for prediction
sample = X.iloc[[0]]

# Predict AQI
predicted_aqi = model.predict(sample)[0]

# Get category and alert
category = get_aqi_category(predicted_aqi)
alert = generate_alert(predicted_aqi)

print("Predicted AQI:", round(predicted_aqi))
print("AQI Category:", category)
print("Health Alert:", alert)