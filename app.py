import streamlit as st
import requests
import pandas as pd

# 1. Define your bailout destinations with their latitude and longitude
DESTINATIONS = {
    "Istanbul (IST)": {"lat": 41.2753, "lon": 28.7520},
    "Munich (MUC)": {"lat": 48.3538, "lon": 11.7861},
    "Milan (MXP)": {"lat": 45.6306, "lon": 8.7281}
}

def get_weather(lat, lon):
    """Fetches a 7-day forecast from the free Open-Meteo API."""
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&daily=temperature_2m_max,temperature_2m_min,precipitation_probability_max&temperature_unit=fahrenheit&timezone=auto"
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.json()
    return None

def main():
    st.set_page_config(page_title="Standby Weather Tracker", layout="wide")
    st.title("🌍 Standby Destination Weather")
    st.write("Tracking 7-day forecasts for potential ZED routes out of HND/NRT.")
    
    st.markdown("---")

    # 2. Create columns for a side-by-side view of all cities
    cols = st.columns(len(DESTINATIONS))
    
    for index, (city, coords) in enumerate(DESTINATIONS.items()):
        with cols[index]:
            st.subheader(city)
            
            # Fetch the data
            weather_data = get_weather(coords["lat"], coords["lon"])
            
            if weather_data and "daily" in weather_data:
                daily = weather_data["daily"]
                
                # Create a clean dataframe for Streamlit
                df = pd.DataFrame({
                    "Date": pd.to_datetime(daily["time"]).strftime('%b %d'),
                    "High (°F)": daily["temperature_2m_max"],
                    "Low (°F)": daily["temperature_2m_min"],
                    "Rain Chance (%)": daily["precipitation_probability_max"]
                })
                
                # Display today's high prominently
                st.metric(
                    label="Today's High", 
                    value=f"{daily['temperature_2m_max'][0]} °F",
                    delta=f"{daily['precipitation_probability_max'][0]}% Rain"
                )
                
                # Display the full week table without the row index
                st.dataframe(df, hide_index=True, use_container_width=True)
                
                # Add a quick visual line chart for the temperature trend
                st.line_chart(df.set_index("Date")[["High (°F)", "Low (°F)"]])
            else:
                st.error("Failed to load weather data.")

if __name__ == "__main__":
    main()