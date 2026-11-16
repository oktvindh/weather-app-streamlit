import streamlit as st
import pandas as pd
import joblib

# 1. Muat model terbaik yang sudah diserialisasi (Subbab 14.14)
@st.cache_resource
def load_model():
    return joblib.load('weather_model_best.pkl')

model = load_model()

# 2. Judul dan Deskripsi Aplikasi
st.title("🌦️ Aplikasi Prediksi Cuaca Esok Hari (WeatherAUS)")
st.write("Masukkan parameter cuaca hari ini untuk memprediksi apakah besok akan turun hujan.")

# 3. Membuat Form Input Pengguna (Widget Streamlit)
col1, col2 = st.columns(2)

with col1:
    min_temp = st.number_input("Suhu Minimum (°C)", value=12.0)
    max_temp = st.number_input("Suhu Maksimum (°C)", value=25.0)
    rainfall = st.number_input("Curah Hujan / Rainfall (mm)", value=0.0)
    humidity_9am = st.slider("Kelembapan Pukul 09:00 (%)", 0, 100, 60)
    humidity_3pm = st.slider("Kelembapan Pukul 15:00 (%)", 0, 100, 40)

with col2:
    wind_gust_speed = st.number_input("Kecepatan Angin Maksimum (km/h)", value=40.0)
    wind_speed_9am = st.number_input("Kecepatan Angin Pukul 09:00 (km/h)", value=15.0)
    wind_speed_3pm = st.number_input("Kecepatan Angin Pukul 15:00 (km/h)", value=20.0)
    pressure_9am = st.number_input("Tekanan Udara Pukul 09:00 (hPa)", value=1015.0)
    pressure_3pm = st.number_input("Tekanan Udara Pukul 15:00 (hPa)", value=1012.0)

location = st.selectbox("Lokasi Stasiun Cuaca", ['Albury', 'Sydney', 'Melbourne', 'Brisbane', 'Perth', 'Darwin', 'Hobart'])
wind_gust_dir = st.selectbox("Arah Angin Maksimum", ['W', 'WNW', 'NW', 'N', 'NE', 'E', 'SE', 'S', 'SW'])
wind_dir_9am = st.selectbox("Arah Angin Pukul 09:00", ['W', 'NW', 'N', 'NE', 'E', 'SE', 'S', 'SW'])
wind_dir_3pm = st.selectbox("Arah Angin Pukul 15:00", ['W', 'NW', 'N', 'NE', 'E', 'SE', 'S', 'SW'])
rain_today = st.selectbox("Apakah Hari Ini Hujan?", ['No', 'Yes'])
month = st.slider("Bulan (1-12)", 1, 12, 6)

# 4. Tombol Eksekusi Prediksi & Penanganan Input
if st.button("Prediksi Cuaca Besok"):
    # Membentuk DataFrame sesuai urutan fitur saat pelatihan model
    input_data = pd.DataFrame([[
        location, min_temp, max_temp, rainfall, 0.0, 0.0,
        wind_gust_dir, wind_gust_speed, wind_dir_9am, wind_dir_3pm,
        wind_speed_9am, wind_speed_3pm, humidity_9am, humidity_3pm,
        pressure_9am, pressure_3pm, 0.0, 0.0, min_temp+2, max_temp-2,
        rain_today, month
    ]], columns=[
        'Location', 'MinTemp', 'MaxTemp', 'Rainfall', 'Evaporation', 'Sunshine',
        'WindGustDir', 'WindGustSpeed', 'WindDir9am', 'WindDir3pm',
        'WindSpeed9am', 'WindSpeed3pm', 'Humidity9am', 'Humidity3pm',
        'Pressure9am', 'Pressure3pm', 'Cloud9am', 'Cloud3pm', 'Temp9am',
        'Temp3pm', 'RainToday', 'Month'
    ])

    # Melakukan inferensi menggunakan model (Subbab 14.5 & 14.14)
    prediksi = model.predict(input_data)[0]
    probabilitas = model.predict_proba(input_data)[0][1]

    # Menampilkan hasil prediksi ke antarmuka
    st.subheader("Hasil Prediksi:")
    if prediksi == 1:
        st.error(f"🌧️ **Besok DIPREDIKSI HUJAN!** (Probabilitas: {probabilitas:.1%})")
    else:
        st.success(f"☀️ **Besok DIPREDIKSI TIDAK HUJAN (Cerah/Berawan).** (Probabilitas Hujan: {probabilitas:.1%})")
