import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import os
# Konfigurasi halaman Streamlit
st.set_page_config(
    page_title="Dashboard Analisis Penyewaan Sepeda",
    page_icon="🚲",
    layout="wide"
)
st.subheader("Daftar File dalam Direktori:")
st.write(os.listdir())



# Membaca data
day_df = pd.read_csv('day.csv')

# Konversi kolom date ke format datetime
day_df['date'] = pd.to_datetime(day_df['dteday'])

# Judul dashboard
st.title("Dashboard Analisis Penyewaan Sepeda (2011-2012)")
st.write("Analisis data peminjaman sepeda berdasarkan berbagai faktor")

# Tampilkan beberapa data awal
st.subheader("Data Peminjaman Sepeda")
st.dataframe(day_df.head())

# Visualisasi tren jumlah peminjaman sepeda harian
st.subheader("Tren Jumlah Peminjam Sepeda Harian")
fig1, ax1 = plt.subplots(figsize=(14, 5))
ax1.plot(day_df['date'], day_df['cnt'], label='Jumlah Peminjam Harian', color='tab:blue', linewidth=1)
ax1.set_title('Tren Jumlah Peminjam Sepeda Harian (2011-2012)')
ax1.set_xlabel('Tanggal')
ax1.set_ylabel('Jumlah Peminjam')
ax1.grid(alpha=0.3)
plt.tight_layout()
st.pyplot(fig1)

# Visualisasi berdasarkan musim
st.subheader("Rata-rata Jumlah Peminjam Sepeda per Musim")
fig2, ax2 = plt.subplots(figsize=(10, 6))
sns.barplot(x='season', y='cnt', data=day_df, estimator=np.mean, errorbar=None, palette='Set2', ax=ax2)
ax2.set_title('Rata-rata Jumlah Peminjam Sepeda per Musim')
ax2.set_xlabel('Musim (1: Semi, 2: Panas, 3: Gugur, 4: Dingin)')
ax2.set_ylabel('Rata-rata Jumlah Peminjam')
plt.tight_layout()
st.pyplot(fig2)

# Visualisasi berdasarkan kondisi cuaca
st.subheader("Pengaruh Kondisi Cuaca Terhadap Peminjaman Sepeda")
fig3, ax3 = plt.subplots(figsize=(10, 6))
sns.barplot(x='weathersit', y='cnt', data=day_df, estimator=np.mean, errorbar=None, palette='Set1', ax=ax3)
ax3.set_title('Rata-rata Jumlah Peminjam Sepeda per Kondisi Cuaca')
ax3.set_xlabel('Kondisi Cuaca (1: Cerah, 2: Mendung, 3: Hujan)')
ax3.set_ylabel('Rata-rata Jumlah Peminjam')
plt.tight_layout()
st.pyplot(fig3)

# Visualisasi berdasarkan hari kerja/libur
st.subheader("Perbandingan Hari Kerja vs Hari Libur")
fig4, ax4 = plt.subplots(figsize=(10, 6))
sns.barplot(x='workingday', y='cnt', data=day_df, estimator=np.mean, errorbar=None, palette='pastel', ax=ax4)
ax4.set_title('Rata-rata Jumlah Peminjam Sepeda (Hari Kerja vs Hari Libur)')
ax4.set_xlabel('Hari Kerja (0: Libur, 1: Kerja)')
ax4.set_ylabel('Rata-rata Jumlah Peminjam')
plt.tight_layout()
st.pyplot(fig4)

# Penjelasan analisis
st.subheader("Penjelasan Analisis")
st.write("""
- **Tren Harian**: Grafik tren harian menunjukkan adanya pola musiman dan peningkatan jumlah peminjam dari tahun 2011 ke 2012.
- **Musim**: Rata-rata jumlah peminjam tertinggi terjadi pada musim panas (season 2 dan 3), dan terendah pada musim dingin (season 4).
- **Cuaca**: Kondisi cuaca sangat memengaruhi jumlah peminjam: cuaca cerah (weathersit=1) menghasilkan peminjaman tertinggi, sedangkan cuaca buruk (weathersit=3) menurunkan jumlah peminjam secara signifikan.
- **Hari Kerja**: Hari kerja (workingday=1) cenderung memiliki jumlah peminjam lebih tinggi dibanding hari libur, menunjukkan banyak pengguna menggunakan sepeda untuk aktivitas rutin.
""")
