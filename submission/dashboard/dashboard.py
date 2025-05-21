import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Konfigurasi halaman Streamlit
st.set_page_config(
    page_title="Dashboard Analisis Penyewaan Sepeda",
    page_icon="🚲",
    layout="wide"
)

# Judul utama
st.title("Dashboard Analisis Penyewaan Sepeda")

# Memuat data
@st.cache_data
def load_data():
    try:
        data = pd.read_csv("dataset/day.csv")
        return data
    except FileNotFoundError:
        st.error("File 'day.csv' tidak ditemukan. Silakan periksa jalur file.")
        return None

data = load_data()

if data is not None:
    # Pra-pemrosesan data
    # Mengubah tanggal menjadi format datetime
    data['dteday'] = pd.to_datetime(data['dteday'])
    
    # Memetakan nilai musim dan cuaca
    season_mapping = {1: 'Musim Dingin', 2: 'Musim Semi', 3: 'Musim Panas', 4: 'Musim Gugur'}
    data['season_name'] = data['season'].map(season_mapping)
    
    weather_mapping = {1: 'Cerah', 2: 'Berkabut', 3: 'Hujan/Salju Ringan', 4: 'Hujan/Salju Lebat'}
    data['weathersit_name'] = data['weathersit'].map(weather_mapping)
    
    # Menampilkan ikhtisar dataset
    st.header("Ikhtisar Dataset")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Pratinjau Dataset")
        st.dataframe(data.head())
    
    with col2:
        st.subheader("Informasi Dataset")
        st.write(f"Jumlah Baris: {data.shape[0]}")
        st.write(f"Jumlah Kolom: {data.shape[1]}")
        
        # Menampilkan statistik dasar
        st.subheader("Ringkasan Statistik")
        st.dataframe(data.describe())
    
    # Membuat tab untuk analisis berbeda
    st.header("Analisis & Wawasan")
    tab1, tab2, tab3, tab4 = st.tabs([
        "Analisis Musiman", 
        "Dampak Cuaca", 
        "Tren Penyewaan", 
        "Analisis Korelasi"
    ])
    
    with tab1:
        st.subheader("Penyewaan Sepeda berdasarkan Musim")
        
        season_data = data.groupby('season_name')['cnt'].mean().reset_index()
        
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.barplot(x='season_name', y='cnt', data=season_data, ax=ax)
        plt.title('Rata-rata Penyewaan Sepeda berdasarkan Musim')
        plt.xlabel('Musim')
        plt.ylabel('Rata-rata Penyewaan')
        plt.xticks(rotation=0)
        st.pyplot(fig)
        
        st.markdown("""
        **Insight:** Musim Panas dan Musim Gugur memiliki jumlah penyewaan sepeda yang lebih tinggi dibandingkan dengan Musim Dingin dan Musim Semi.
        Ini menunjukkan preferensi musiman untuk bersepeda ketika cuaca lebih mendukung.
        """)
    
    with tab2:
        st.subheader("Dampak Cuaca pada Penyewaan Sepeda")
        
        weather_data = data.groupby('weathersit_name')['cnt'].mean().reset_index()
        
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.barplot(x='weathersit_name', y='cnt', data=weather_data, ax=ax)
        plt.title('Rata-rata Penyewaan Sepeda berdasarkan Kondisi Cuaca')
        plt.xlabel('Kondisi Cuaca')
        plt.ylabel('Rata-rata Penyewaan')
        plt.xticks(rotation=45)
        st.pyplot(fig)
        
        st.markdown("""
        **Insight:** Kondisi cuaca secara signifikan mempengaruhi pola penyewaan sepeda.
        Cuaca Cerah memiliki rata-rata penyewaan tertinggi, sementara Hujan/Salju Lebat menunjukkan jumlah penyewaan terendah.
        """)
    
    with tab3:
        st.subheader("Tren Penyewaan Sepeda Sepanjang Waktu")
        
        # Tren bulanan
        data['month'] = data['dteday'].dt.month
        data['year'] = data['dteday'].dt.year
        
        monthly_data = data.groupby(['year', 'month'])['cnt'].sum().reset_index()
        
        fig, ax = plt.subplots(figsize=(12, 6))
        for year in monthly_data['year'].unique():
            year_data = monthly_data[monthly_data['year'] == year]
            plt.plot(year_data['month'], year_data['cnt'], marker='o', label=f'Tahun {year}')
        
        plt.title('Tren Penyewaan Sepeda Bulanan')
        plt.xlabel('Bulan')
        plt.ylabel('Total Penyewaan')
        plt.xticks(range(1, 13))
        plt.legend()
        plt.grid(True, alpha=0.3)
        st.pyplot(fig)
        
        st.markdown("""
        **Insight:** Penyewaan sepeda menunjukkan pola musiman yang jelas dengan puncaknya selama bulan-bulan musim panas.
        Terdapat juga tren pertumbuhan secara keseluruhan dari tahun ke tahun, menunjukkan popularitas layanan yang meningkat.
        """)
    
    with tab4:
        st.subheader("Korelasi Antar Faktor")
        
        # Pilih hanya kolom numerik untuk analisis korelasi
        numeric_cols = ['temp', 'atemp', 'hum', 'windspeed', 'cnt', 'casual', 'registered']
        corr_data = data[numeric_cols]
        
        fig, ax = plt.subplots(figsize=(12, 10))
        correlation = corr_data.corr()
        sns.heatmap(correlation, annot=True, cmap='coolwarm', fmt=".2f", ax=ax)
        plt.title("Peta Panas Korelasi")
        st.pyplot(fig)
        
        st.markdown("""
        **Insight:** Suhu menunjukkan korelasi positif yang kuat dengan penyewaan sepeda.
        Kelembaban menunjukkan korelasi negatif, menunjukkan bahwa orang cenderung tidak menyewa sepeda dalam kondisi lembab.
        Pengguna terdaftar berkontribusi lebih banyak terhadap total penyewaan dibandingkan pengguna kasual.
        """)
    
    # Bagian eksplorasi interaktif
    st.header("Eksplorasi Interaktif")
    
    explore_col1, explore_col2 = st.columns(2)
    
    with explore_col1:
        st.subheader("Penyewaan berdasarkan Jenis Hari")
        workingday_data = data.groupby('workingday')['cnt'].mean().reset_index()
        workingday_data['day_type'] = workingday_data['workingday'].map({0: 'Akhir Pekan/Libur', 1: 'Hari Kerja'})
        
        fig, ax = plt.subplots(figsize=(8, 5))
        sns.barplot(x='day_type', y='cnt', data=workingday_data, ax=ax)
        plt.title('Rata-rata Penyewaan berdasarkan Jenis Hari')
        plt.xlabel('Jenis Hari')
        plt.ylabel('Rata-rata Penyewaan')
        st.pyplot(fig)
    
    with explore_col2:
        st.subheader("Suhu vs. Penyewaan")
        
        fig, ax = plt.subplots(figsize=(8, 5))
        sns.scatterplot(x='temp', y='cnt', hue='season_name', data=data, ax=ax)
        plt.title('Suhu vs. Total Penyewaan')
        plt.xlabel('Suhu (Dinormalisasi)')
        plt.ylabel('Total Penyewaan')
        st.pyplot(fig)
    
    # Tambahkan sidebar filter
    st.sidebar.header("Filter")
    
    # Filter berdasarkan musim
    selected_seasons = st.sidebar.multiselect(
        "Pilih Musim", 
        options=list(season_mapping.values()),
        default=list(season_mapping.values())
    )
    
    # Filter berdasarkan cuaca
    selected_weather = st.sidebar.multiselect(
        "Pilih Kondisi Cuaca", 
        options=list(weather_mapping.values()),
        default=list(weather_mapping.values())
    )
    
    # Filter berdasarkan tahun
    years = sorted(data['dteday'].dt.year.unique())
    selected_years = st.sidebar.multiselect("Pilih Tahun", options=years, default=years)
    
    # Terapkan filter
    filtered_data = data.copy()
    if selected_seasons:
        filtered_data = filtered_data[filtered_data['season_name'].isin(selected_seasons)]
    if selected_weather:
        filtered_data = filtered_data[filtered_data['weathersit_name'].isin(selected_weather)]
    if selected_years:
        filtered_data = filtered_data[filtered_data['dteday'].dt.year.isin(selected_years)]
    
    # Tampilkan hasil filter
    st.header("Hasil Filter")
    st.dataframe(filtered_data)
    
    # Bagian tentang di sidebar
    st.sidebar.header("Tentang")
    st.sidebar.info("""
    Dashboard ini menyediakan analisis dataset penyewaan sepeda.
    
    Data menunjukkan jumlah penyewaan sepeda harian beserta kondisi cuaca dan informasi musiman.
    
    Gunakan filter di sebelah kiri untuk berinteraksi dengan visualisasi.
    """)

else:
    st.warning("Silakan periksa bahwa file dataset ada di lokasi yang benar.")
