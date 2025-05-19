import streamlit as st
import streamlit.components.v1 as components
import datetime
import requests

API_KEY = 'bd5e378503939ddaee76f12ad7a97608'

def get_browser_time():
    js_code = """
    <script>
        const currentTime = new Date();
        const timeStr = currentTime.toISOString();
        document.body.innerText = timeStr;
    </script>
    """
    time_str = components.html(js_code, height=30)
    return time_str

def get_weather(city):
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric'
    response = requests.get(url)
    return response.json()

def main():
    st.title("Weather & Time Finder")
    city = st.text_input("Enter a city name")

    if city:
        data = get_weather(city)
        if data.get("cod") != 200:
            st.error(f"City not found: {data.get('message', '')}")
            return

        utc_now = datetime.datetime.utcnow()
        city_offset_sec = data['timezone']
        city_time = utc_now + datetime.timedelta(seconds=city_offset_sec)

        st.write(f"**City Local Time:** {city_time.strftime('%A, %Y-%m-%d %H:%M:%S')}")

        st.warning("Accurate local device time not available via Python directly. Try deploying locally or using JS to fetch it.")

if __name__ == '__main__':
    main()
