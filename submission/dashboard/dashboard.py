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
    day_df = pd.read_csv('day.csv')
    # Convert date column to datetime
    day_df['date'] = pd.to_datetime(day_df['dteday'])
    return day_df

# Load the data
day_df = load_data()

# Part 1: Daily Bike Rental Trend
st.header("1. Tren Jumlah Peminjaman Sepeda Harian (2011-2012)")

fig1, ax1 = plt.subplots(figsize=(14, 5))
ax1.plot(day_df['date'], day_df['cnt'], label='Jumlah Peminjam Harian', color='tab:blue', linewidth=1)
ax1.set_title('Tren Jumlah Peminjam Sepeda Harian (2011-2012)')
ax1.set_xlabel('Tanggal')
ax1.set_ylabel('Jumlah Peminjam')
ax1.grid(alpha=0.3)
plt.tight_layout()
st.pyplot(fig1)

# Part 2: Average Rentals by Season
st.header("2. Rata-rata Jumlah Peminjam Sepeda per Musim")
# Map season values to names for better readability
season_names = {1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'}
day_df['season_name'] = day_df['season'].map(season_names)

fig2, ax2 = plt.subplots(figsize=(10, 6))
sns.barplot(x='season', y='cnt', hue='season', data=day_df, estimator=np.mean, errorbar=None, palette='Set2', ax=ax2)
ax2.set_title('Rata-rata Jumlah Peminjam Sepeda per Musim')
ax2.set_xlabel('Musim (1: Semi, 2: Panas, 3: Gugur, 4: Dingin)')
ax2.set_ylabel('Rata-rata Jumlah Peminjam')
plt.tight_layout()
st.pyplot(fig2)

# Part 3: Average Rentals by Weather Condition
st.header("3. Rata-rata Jumlah Peminjam Sepeda per Kondisi Cuaca")
# Map weather situation values to names
weather_names = {1: 'Clear', 2: 'Cloudy', 3: 'Light Rain/Snow', 4: 'Heavy Rain/Snow'}
day_df['weather_name'] = day_df['weathersit'].map(weather_names)

fig3, ax3 = plt.subplots(figsize=(10, 6))
sns.barplot(x='weathersit', y='cnt', hue='weathersit', data=day_df, estimator=np.mean, errorbar=None, palette='Set1', ax=ax3)
ax3.set_title('Rata-rata Jumlah Peminjam Sepeda per Kondisi Cuaca')
ax3.set_xlabel('Kondisi Cuaca (1: Cerah, 2: Mendung, 3: Hujan/Salju Ringan, 4: Hujan/Salju Lebat)')
ax3.set_ylabel('Rata-rata Jumlah Peminjam')
plt.tight_layout()
st.pyplot(fig3)

# Part 4: Average Rentals by Working Day
st.header("4. Rata-rata Jumlah Peminjam Sepeda (Hari Kerja vs Hari Libur)")

fig4, ax4 = plt.subplots(figsize=(10, 6))
sns.barplot(x='workingday', y='cnt', hue='workingday', data=day_df, estimator=np.mean, errorbar=None, palette='pastel', ax=ax4)
ax4.set_title('Rata-rata Jumlah Peminjam Sepeda (Hari Kerja vs Hari Libur)')
ax4.set_xlabel('Hari Kerja (0: Libur, 1: Kerja)')
ax4.set_ylabel('Rata-rata Jumlah Peminjam')
plt.tight_layout()
st.pyplot(fig4)

# Conclusions
st.header("Kesimpulan")
st.write("""
**Penjelasan:**
- Grafik tren harian menunjukkan adanya pola musiman dan peningkatan jumlah peminjam dari tahun 2011 ke 2012.
- Rata-rata jumlah peminjam tertinggi terjadi pada musim panas (season 2 dan 3), dan terendah pada musim dingin (season 4).
- Kondisi cuaca sangat memengaruhi jumlah peminjam: cuaca cerah (weathersit=1) menghasilkan peminjaman tertinggi, sedangkan cuaca buruk (weathersit=3) menurunkan jumlah peminjam secara signifikan.
- Hari kerja (workingday=1) cenderung memiliki jumlah peminjam lebih tinggi dibanding hari libur, menunjukkan banyak pengguna menggunakan sepeda untuk aktivitas rutin.
""")
