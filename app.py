import streamlit as st
import requests
from datetime import datetime, timedelta

API_KEY = 'bd5e378503939ddaee76f12ad7a97608'

def get_weather(city):
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric'
    response = requests.get(url)
    return response.json()

def main():
    st.set_page_config(page_title="Weather & Time Finder", layout="centered")
    st.title("Weather & Time Finder")

    city = st.text_input("Enter a city name")

    if city:
        data = get_weather(city)
        if data.get("cod") != 200:
            st.error(f"City not found: {data.get('message', '')}")
            return

        st.success(f"Location: {data['name']}, {data['sys']['country']}")
        st.write(f"**Weather:** {data['weather'][0]['description'].title()}")
        st.write(f"**Temperature:** {data['main']['temp']} °C")

        # City time using timezone offset (in seconds)
        timezone_offset_sec = data['timezone']
        utc_now = datetime.utcnow()
        city_time = utc_now + timedelta(seconds=timezone_offset_sec)
        formatted_city_time = city_time.strftime("%A, %Y-%m-%d %H:%M:%S")

        # Local device time
        local_time = datetime.now()
        formatted_local_time = local_time.strftime("%A, %Y-%m-%d %H:%M:%S")

        st.write(f"**Local Time (Your Device):** {formatted_local_time}")
        st.write(f"**Local Time in {city}:** {formatted_city_time}")

        # Time difference in hours
        time_diff_hours = (city_time - local_time).total_seconds() / 3600
        if abs(time_diff_hours) < 0.01:
            time_diff_msg = "Same time zone as your device"
        else:
            time_diff_msg = f"{abs(time_diff_hours):.1f} hour(s) {'ahead' if time_diff_hours > 0 else 'behind'} your local time"

        st.write(f"**Time Difference:** {time_diff_msg}")

if __name__ == '__main__':
    main()
