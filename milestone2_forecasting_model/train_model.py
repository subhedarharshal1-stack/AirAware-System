import joblib
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score


# Load dataset
df = pd.read_csv("data/air_quality.csv")

# Drop rows where AQI is missing
df = df.dropna(subset=["AQI"])

# Select numeric features
df_numeric = df.select_dtypes(include=["number"])

# Features and target
X = df_numeric.drop("AQI", axis=1)
y = df_numeric["AQI"]

# Train test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Create model
model = RandomForestRegressor(n_estimators=100, random_state=42)

# Train model
model.fit(X_train, y_train)



joblib.dump(model, "milestone2_forecasting_model/aqi_model.pkl")
print("Model saved successfully")

# Predict
predictions = model.predict(X_test)

# Evaluate model
mae = mean_absolute_error(y_test, predictions)
r2 = r2_score(y_test, predictions)

print("Model Training Completed")
print("MAE:", mae)
print("R2 Score:", r2)