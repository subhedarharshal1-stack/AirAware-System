import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load dataset
df = pd.read_csv("data/air_quality.csv")

# Convert Date column
df["Date"] = pd.to_datetime(df["Date"])

# Extract month
df["Month"] = df["Date"].dt.month

# Remove missing AQI values
df = df.dropna(subset=["AQI"])

# Monthly AQI average
monthly_trend = df.groupby("Month")["AQI"].mean()

print("Monthly AQI Trend:")
print(monthly_trend)

# Plot monthly trend
plt.figure(figsize=(10,5))
sns.lineplot(x=monthly_trend.index, y=monthly_trend.values)

plt.title("Monthly AQI Trend")
plt.xlabel("Month")
plt.ylabel("Average AQI")

plt.show()