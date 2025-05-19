import streamlit as st
import streamlit.components.v1 as components
import requests
from datetime import datetime, timedelta
import json

API_KEY = 'bd5e378503939ddaee76f12ad7a97608'

# JavaScript to get device location and local time
def get_user_location_and_time():
    js_code = """
    <script>
        const sendData = () => {
            const date = new Date();
            const localTime = date.toISOString();
            navigator.geolocation.getCurrentPosition((pos) => {
                const coords = {
                    lat: pos.coords.latitude,
                    lon: pos.coords.longitude,
                    time: localTime
                };
                const data = JSON.stringify(coords);
                const iframe = document.createElement('iframe');
                iframe.setAttribute('srcdoc', `<script>
                    window.parent.postMessage(${JSON.stringify(data)}, '*');
                </script>`);
                document.body.appendChild(iframe);
            });
        };
        sendData();
    </script>
    """
    result = components.html(js_code, height=0)
    return result

# Streamlit listener for JavaScript messages
def get_coordinates_from_message():
    coords = st.experimental_get_query_params().get("msg", [None])[0]
    if coords:
        try:
            return json.loads(coords)
        except:
            return None
    return None

def get_weather(city):
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric'
    return requests.get(url).json()

# UI and logic
def main():
    st.set_page_config(page_title="Live Weather & Time App", layout="centered")
    st.title("Weather, Time & Difference Tracker")

    # JavaScript to capture user's browser location and time
    st.subheader("Step 1: Getting Your Device Info")
    get_user_location_and_time()
    st.info("Please allow location access in your browser to fetch accurate time.")

    city = st.text_input("Step 2: Enter any city name to compare")

    if city:
        data = get_weather(city)
        if data.get("cod") != 200:
            st.error(f"City not found: {data.get('message', '')}")
            return

        st.success(f"City: {data['name']}, {data['sys']['country']}")
        st.write(f"**Weather:** {data['weather'][0]['description'].title()}")
        st.write(f"**Temperature:** {data['main']['temp']} °C")

        # City local time
        city_offset = data['timezone']
        utc_now = datetime.utcnow()
        city_time = utc_now + timedelta(seconds=city_offset)
        st.write(f"**Local Time in {city}:** {city_time.strftime('%A, %Y-%m-%d %H:%M:%S')}")

        # Fallback method (warns user)
        st.warning("Time difference will be calculated using device time only if permission is granted. Otherwise, fallback is UTC.")
        
        # Use datetime.now() as an approximation for local time
        device_time = datetime.now()
        st.write(f"**Your Device's Local Time:** {device_time.strftime('%A, %Y-%m-%d %H:%M:%S')}")

        # Time difference
        time_diff_hours = (city_time - device_time).total_seconds() / 3600
        if abs(time_diff_hours) < 0.01:
            diff_msg = "Same time zone as your device"
        else:
            diff_msg = f"{abs(time_diff_hours):.1f} hour(s) {'ahead' if time_diff_hours > 0 else 'behind'} your local time"

        st.write(f"**Time Difference:** {diff_msg}")

if __name__ == '__main__':
    main()
