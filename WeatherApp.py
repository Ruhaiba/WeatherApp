import sqlite3
import streamlit as st
from datetime import date
import pandas as pd
import requests

#Setting up our database using sqlite3
weather_data = sqlite3.connect("weather_data.db")

cur = weather_data.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS information
            (id integer PRIMARY KEY AUTOINCREMENT, 
            country text, 
            city text UNIQUE)''')

weather_data.commit()

#Web development using streamlit

st.title("WeatherApp")

df = pd.read_csv("worldcities.csv")

cntries = df["country"].unique() 
selected_country = st.selectbox("Select Country:", cntries)
cities_in_cntries = df[df["country"] == selected_country]["city"].tolist()
selected_city= st.selectbox("Select City", cities_in_cntries)
day = date.today()
            
if st.button("DELETE LOCATION"):
    cur.execute("DELETE FROM information WHERE city = ?", (selected_city,))
    weather_data.commit()
    st.success("LOCATION DELETED")
    
if st.button("VIEW LOCATION DATA"):
    cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
    st.write("Tables:", cur.fetchall())

    cur.execute("SELECT * FROM information;")
    rows = cur.fetchall()
    st.write("Rows:", rows)
    
if st.button("SAVE EVERYTHING ABOVE"):
    existo = cur.fetchone()
    if existo:
        skip=True
    else:
        cur.execute("INSERT OR IGNORE INTO information ( country, city) VALUES ( ?, ?)",
                    (selected_country, selected_city))
        weather_data.commit()
        st.success("EVERYTHING ABOVE SAVED SUCCESSFULLY")
    
    #Using the API key (From OpenWeatherMap)
    
    api_key =  "914a06ca76a02205b19d95c459cf3f06"
    url_api = f"https://api.openweathermap.org/data/2.5/forecast?q={selected_city}&units=metric&appid={api_key}"
    resp = requests.get(url_api)

    if resp.status_code == 200:
        data = resp.json()
        disp_days = set()
        count = 0
        
        daily_forecast = {} 
        for x in data["list"]:
            time = x["dt_txt"].split(" ")[0]
            if time not in daily_forecast:
                daily_forecast[time] = x
        
        for day, x in list(daily_forecast.items())[:5]:
            temperature = x["main"]["temp"]
            desc = x["weather"][0]["description"]
            d1 = x["dt_txt"].split(" ")[0]
            d1 = str(d1)
            d1 = d1[0:]
            st.write(f"DAY OF THE WEEK: {d1}")
            st.write(f"TEMPERATURE: {temperature}°C")
            st.write(f"CONDITION: {desc}")
            st.write("----------------------------------------------------------------------------------------------------")
    else:
        st.write("Something went wrong, developer will deal with it.")
        
#descripto
st.write("")
st.write("")
st.write("")
st.write("")
st.write("")
st.write("RUHAIBA AHMAD - DEVELOPER")
st.write("Hello! Welcome to WeatherApp, a application that gives")
st.write("a 5 day forecast of any country and city you choose!")
st.write("This application was not built to look good, but to work,")
st.write("as I prefer functionality > looks. This app was made using")
st.write("Streamlit and sqlite3. I hope this application will be of assist")
st.write("Thanks for using WeatherApp!")

    

