import streamlit as st
import requests
from datetime import datetime, timedelta, timezone

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

        # Get target city time using UTC + offset
        timezone_offset_sec = data['timezone']
        utc_now = datetime.utcnow().replace(tzinfo=timezone.utc)
        city_time = utc_now + timedelta(seconds=timezone_offset_sec)
        formatted_city_time = city_time.strftime("%A, %Y-%m-%d %H:%M:%S")
        st.write(f"**Local Time in {city}:** {formatted_city_time}")

        # Get device local time and offset
        device_time = datetime.now().astimezone()
        device_offset_sec = device_time.utcoffset().total_seconds()

        # Time difference
        diff_hours = (timezone_offset_sec - device_offset_sec) / 3600
        if diff_hours == 0:
            time_diff_msg = "Same time zone as your device"
        else:
            time_diff_msg = f"{abs(diff_hours):.1f} hour(s) {'ahead' if diff_hours > 0 else 'behind'} your local time"

        st.write(f"**Time Difference:** {time_diff_msg}")
        st.write(f"**Your Local Time:** {device_time.strftime('%A, %Y-%m-%d %H:%M:%S')}")

if __name__ == '__main__':
    main()
