def generate_alert(aqi):

    if aqi > 300:
        return "☠ Hazardous Air! Stay indoors."
    elif aqi > 200:
        return "⚠ Very Unhealthy! Avoid outdoor activities."
    elif aqi > 150:
        return "⚠ Unhealthy! Wear a mask outside."
    elif aqi > 100:
        return "Moderate air quality. Sensitive groups be careful."
    else:
        return "Air quality is safe."


# Test example
if __name__ == "__main__":

    sample_aqi = [45, 120, 170, 220, 350]

    for value in sample_aqi:
        alert = generate_alert(value)
        print(f"AQI: {value} → {alert}")