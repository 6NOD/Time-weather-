import streamlit as st
import requests
from datetime import datetime

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

        # Calculate time in target location
        timezone_offset = data['timezone']  # in seconds
        utc_now = datetime.utcnow().timestamp()
        local_timestamp = utc_now + timezone_offset
        local_time = datetime.fromtimestamp(local_timestamp)
        formatted_time = local_time.strftime("%A, %Y-%m-%d %H:%M:%S")
        st.write(f"**Local Time in {city}:** {formatted_time}")

        # Time difference calculation
        local_offset_hrs = -datetime.now().astimezone().utcoffset().total_seconds() / 3600
        city_offset_hrs = timezone_offset / 3600
        diff = city_offset_hrs - local_offset_hrs

        if diff == 0:
            time_diff_msg = "Same time zone as your device"
        else:
            time_diff_msg = f"{abs(diff):.1f} hour(s) {'ahead' if diff > 0 else 'behind'} your local time"

        st.write(f"**Time Difference:** {time_diff_msg}")

if __name__ == '__main__':
    main()
