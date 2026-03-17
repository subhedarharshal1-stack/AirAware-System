def get_aqi_category(aqi):

    if aqi <= 50:
        return "Good"
    elif aqi <= 100:
        return "Moderate"
    elif aqi <= 200:
        return "Unhealthy"
    elif aqi <= 300:
        return "Very Unhealthy"
    else:
        return "Hazardous"


# Test example
if __name__ == "__main__":

    sample_aqi = [45, 90, 150, 250, 350]

    for value in sample_aqi:
        category = get_aqi_category(value)
        print(f"AQI: {value} → Category: {category}")