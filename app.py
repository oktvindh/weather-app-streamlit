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
    # Buat dictionary atau DataFrame dengan kolom yang persis sama seperti saat training
    input_data = pd.DataFrame({
        'Location': [location],
        'MinTemp': [min_temp],
        'MaxTemp': [max_temp],
        'Rainfall': [rainfall],
        'Evaporation': [0.0],  # Nilai default jika tidak diinput di UI
        'Sunshine': [0.0],
        'WindGustDir': [wind_gust_dir],
        'WindGustSpeed': [wind_gust_speed],
        'WindDir9am': [wind_dir_9am],
        'WindDir3pm': [wind_dir_3pm],
        'WindSpeed9am': [wind_speed_9am],
        'WindSpeed3pm': [wind_speed_3pm],
        'Humidity9am': [humidity_9am],
        'Humidity3pm': [humidity_3pm],
        'Pressure9am': [pressure_9am],
        'Pressure3pm': [pressure_3pm],
        'Cloud9am': [0.0],
        'Cloud3pm': [0.0],
        'Temp9am': [min_temp + 2],  # Estimasi perkiraan suhu pagi
        'Temp3pm': [max_temp - 2],  # Estimasi perkiraan suhu sore
        'RainToday': [rain_today],
        'Month': [month]
})
    
    # Lakukan Prediksi
    prediksi = model.predict(input_data)[0]
    probabilitas = model.predict_proba(input_data)[0][1]
    
    st.subheader("Hasil Prediksi:")
    if prediksi == 1:
        st.error(f"🌧️ **Besok DIPREDIKSI HUJAN!** (Probabilitas: {probabilitas:.1%})")
    else:
        st.success(f"☀️ **Besok DIPREDIKSI TIDAK HUJAN (Cerah/Berawan).** (Probabilitas Hujan: {probabilitas:.1%})")