import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import os

import matplotlib.pyplot as plt

# Set page title and configuration
st.set_page_config(
    page_title="Bike Sharing Dashboard",
    layout="wide"
)

# Title of the dashboard
st.title("Bike Sharing Analysis Dashboard")

# Load dataset (adjust the path to where your processed dataset is stored)
@st.cache_data
def load_data():
    base_dir = os.path.dirname(__file__)  
    csv_path = os.path.join(base_dir, "day.csv")
    day_df = pd.read_csv(csv_path)
    day_df['date'] = pd.to_datetime(day_df['dteday'])
    return day_df


# Load the data
day_df = load_data()

# Memetakan nilai musim dan cuaca ke nama untuk keterbacaan yang lebih baik
season_names = {1: 'Musim Semi', 2: 'Musim Panas', 3: 'Musim Gugur', 4: 'Musim Dingin'}
day_df['season_name'] = day_df['season'].map(season_names)

weather_names = {1: 'Cerah', 2: 'Berawan', 3: 'Hujan/Salju Ringan', 4: 'Hujan/Salju Lebat'}
day_df['weather_name'] = day_df['weathersit'].map(weather_names)

# Filter sidebar
st.sidebar.header("Filter Data")

# Date filter
min_date = day_df['date'].min().date()
max_date = day_df['date'].max().date()
start_date, end_date = st.sidebar.date_input(
    "Rentang Tanggal",
    [min_date, max_date],
    min_value=min_date,
    max_value=max_date
)

# Season filter
selected_seasons = st.sidebar.multiselect(
    "Pilih Musim",
    options=list(season_names.values()),
    default=list(season_names.values())
)

# Weather filter
selected_weather = st.sidebar.multiselect(
    "Pilih Kondisi Cuaca",
    options=list(weather_names.values()),
    default=list(weather_names.values())
)

# Working day filter
working_day_options = ["Hari Kerja", "Hari Libur", "Semua"]
selected_working_day = st.sidebar.radio("Status Hari", working_day_options)

# Apply filters
filtered_df = day_df.copy()

# Date filter
filtered_df = filtered_df[(filtered_df['date'].dt.date >= start_date) & 
                           (filtered_df['date'].dt.date <= end_date)]

# Season filter
if selected_seasons:
    filtered_df = filtered_df[filtered_df['season_name'].isin(selected_seasons)]

# Weather filter
if selected_weather:
    filtered_df = filtered_df[filtered_df['weather_name'].isin(selected_weather)]

# Working day filter
if selected_working_day == "Hari Kerja":
    filtered_df = filtered_df[filtered_df['workingday'] == 1]
elif selected_working_day == "Hari Libur":
    filtered_df = filtered_df[filtered_df['workingday'] == 0]

# Visualization tabs
tab1, tab2, tab3, tab4 = st.tabs(["Tren Harian", "Analisis Musim", "Analisis Cuaca", "Analisis Hari Kerja"])

with tab1:
    st.header("Tren Jumlah Peminjaman Sepeda Harian")
    
    if not filtered_df.empty:
        fig1, ax1 = plt.subplots(figsize=(14, 5))
        ax1.plot(filtered_df['date'], filtered_df['cnt'], label='Jumlah Peminjam Harian', color='tab:blue', linewidth=1)
        ax1.set_title('Tren Jumlah Peminjam Sepeda Harian')
        ax1.set_xlabel('Tanggal')
        ax1.set_ylabel('Jumlah Peminjam')
        ax1.grid(alpha=0.3)
        plt.tight_layout()
        st.pyplot(fig1)
    else:
        st.warning("Tidak ada data yang sesuai dengan filter yang dipilih.")

with tab2:
    st.header("Rata-rata Jumlah Peminjam Sepeda per Musim")
    
    if not filtered_df.empty:
        fig2, ax2 = plt.subplots(figsize=(10, 6))
        seasonal_avg = filtered_df.groupby('season_name')['cnt'].mean().reset_index()
        sns.barplot(x='season_name', y='cnt', data=seasonal_avg, palette='Set2', ax=ax2)
        ax2.set_title('Rata-rata Jumlah Peminjam Sepeda per Musim')
        ax2.set_xlabel('Musim')
        ax2.set_ylabel('Rata-rata Jumlah Peminjam')
        plt.tight_layout()
        st.pyplot(fig2)
    else:
        st.warning("Tidak ada data yang sesuai dengan filter yang dipilih.")

with tab3:
    st.header("Rata-rata Jumlah Peminjam Sepeda per Kondisi Cuaca")
    
    if not filtered_df.empty:
        fig3, ax3 = plt.subplots(figsize=(10, 6))
        weather_avg = filtered_df.groupby('weather_name')['cnt'].mean().reset_index()
        sns.barplot(x='weather_name', y='cnt', data=weather_avg, palette='Set1', ax=ax3)
        ax3.set_title('Rata-rata Jumlah Peminjam Sepeda per Kondisi Cuaca')
        ax3.set_xlabel('Kondisi Cuaca')
        ax3.set_ylabel('Rata-rata Jumlah Peminjam')
        plt.tight_layout()
        st.pyplot(fig3)
    else:
        st.warning("Tidak ada data yang sesuai dengan filter yang dipilih.")

with tab4:
    st.header("Rata-rata Jumlah Peminjam Sepeda (Hari Kerja vs Hari Libur)")

    if not filtered_df.empty:
        # Menambahkan kolom kategori untuk jenis hari
        filtered_df['day_type'] = filtered_df['workingday'].map({0: 'Hari Libur', 1: 'Hari Kerja'})
    
        # Membuat figure
        fig4, ax4 = plt.subplots(figsize=(6, 4))
    
        # Membuat barplot rata-rata peminjaman
        sns.barplot(
        x='day_type', 
        y='cnt', 
        data=filtered_df, 
        estimator=np.mean, 
        errorbar=None, 
        palette='pastel',
        ax=ax4
    )
    
        # Menyesuaikan elemen visual
        ax4.set_title('Rata-rata Jumlah Peminjam Sepeda\n(Hari Kerja vs Hari Libur)', fontsize=12)
        ax4.set_xlabel('Jenis Hari')
        ax4.set_ylabel('Rata-rata Jumlah Peminjam')
        ax4.set_xticklabels(ax4.get_xticklabels(), fontsize=10)
        ax4.set_yticklabels(ax4.get_yticks(), fontsize=10)
        ax4.grid(axis='y', linestyle='--', alpha=0.5)
    
        # Hilangkan legend (karena hanya 1 variabel kategori)
        ax4.legend([], [], frameon=False)
    
        # Tampilkan di Streamlit
        st.pyplot(fig4)
    else:
        st.warning("Tidak ada data yang sesuai dengan filter yang dipilih.")

# Kesimpulan
st.header("Kesimpulan")
st.write("""
**Penjelasan:**
- Grafik tren harian menunjukkan adanya pola musiman dan peningkatan jumlah peminjam dari tahun 2011 ke 2012.
- Rata-rata jumlah peminjam tertinggi terjadi pada musim panas dan gugur, dan terendah pada musim dingin.
- Kondisi cuaca sangat memengaruhi jumlah peminjam: cuaca cerah menghasilkan peminjaman tertinggi, sedangkan cuaca buruk menurunkan jumlah peminjam secara signifikan.
- Hari kerja cenderung memiliki jumlah peminjam lebih tinggi dibanding hari libur, menunjukkan banyak pengguna menggunakan sepeda untuk aktivitas rutin.
""")
