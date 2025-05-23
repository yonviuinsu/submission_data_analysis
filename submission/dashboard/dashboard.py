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

# Memetakan nilai kondisi cuaca ke nama yang lebih deskriptif
weather_names = {1: 'Cerah', 2: 'Berawan', 3: 'Hujan/Salju Ringan', 4: 'Hujan/Salju Lebat'}
day_df['weather_name'] = day_df['weathersit'].map(weather_names)

# Membuat bagian filter di sidebar
st.sidebar.header("Filter Data")

# Filter untuk rentang tanggal
min_date = day_df['date'].min().date()
max_date = day_df['date'].max().date()
start_date, end_date = st.sidebar.date_input(
    "Rentang Tanggal",
    [min_date, max_date],
    min_value=min_date,
    max_value=max_date
)

# Filter untuk pemilihan musim
selected_seasons = st.sidebar.multiselect(
    "Pilih Musim",
    options=list(season_names.values()),
    default=list(season_names.values())
)

# Filter untuk kondisi cuaca
selected_weather = st.sidebar.multiselect(
    "Pilih Kondisi Cuaca",
    options=list(weather_names.values()),
    default=list(weather_names.values())
)

# Filter untuk hari kerja/libur
working_day_options = ["Hari Kerja", "Hari Libur", "Semua"]
selected_working_day = st.sidebar.radio("Status Hari", working_day_options)

# Menerapkan filter ke dataframe
filtered_df = day_df.copy()

# Menerapkan filter tanggal
filtered_df = filtered_df[(filtered_df['date'].dt.date >= start_date) & 
                           (filtered_df['date'].dt.date <= end_date)]

# Menerapkan filter musim
if selected_seasons:
    filtered_df = filtered_df[filtered_df['season_name'].isin(selected_seasons)]

# Menerapkan filter cuaca
if selected_weather:
    filtered_df = filtered_df[filtered_df['weather_name'].isin(selected_weather)]

# Menerapkan filter hari kerja/libur
if selected_working_day == "Hari Kerja":
    filtered_df = filtered_df[filtered_df['workingday'] == 1]
elif selected_working_day == "Hari Libur":
    filtered_df = filtered_df[filtered_df['workingday'] == 0]

# Bagian Pertanyaan Analisis 1: Faktor-faktor yang mempengaruhi jumlah peminjaman sepeda
st.header("Analisis Tren dan Faktor yang Mempengaruhi Peminjaman Sepeda")

if not filtered_df.empty:
    st.subheader("Pertanyaan: Bagaimana tren jumlah peminjaman sepeda harian selama dua tahun terakhir, dan faktor apa saja yang memengaruhinya (musim, cuaca, hari kerja/libur)?")
    
    # Menggunakan tabs untuk visualisasi pertama
    trend_tabs = st.tabs(["Tren Harian", "Berdasarkan Musim", "Berdasarkan Cuaca", "Hari Kerja vs Libur"])
    
    # Tab 1: Tren Harian
    with trend_tabs[0]:
        st.subheader("Tren Jumlah Peminjaman Sepeda Harian")
        fig1, ax1 = plt.subplots(figsize=(10, 5))
        ax1.plot(filtered_df['date'], filtered_df['cnt'], label='Jumlah Peminjam Harian', color='tab:blue', linewidth=1)
        ax1.set_title('Tren Jumlah Peminjam Sepeda Harian')
        ax1.set_xlabel('Tanggal')
        ax1.set_ylabel('Jumlah Peminjam')
        ax1.grid(alpha=0.3)
        plt.tight_layout()
        st.pyplot(fig1)
    
    # Tab 2: Berdasarkan Musim
    with trend_tabs[1]:
        st.subheader("Rata-rata Jumlah Peminjam per Musim")
        fig2, ax2 = plt.subplots(figsize=(10, 5))
        seasonal_avg = filtered_df.groupby('season_name')['cnt'].mean().reset_index()
        sns.barplot(x='season_name', y='cnt', data=seasonal_avg, palette='Set2', ax=ax2)
        ax2.set_title('Rata-rata Jumlah Peminjam Sepeda per Musim')
        ax2.set_xlabel('Musim')
        ax2.set_ylabel('Rata-rata Jumlah Peminjam')
        plt.tight_layout()
        st.pyplot(fig2)
    
    # Tab 3: Berdasarkan Kondisi Cuaca
    with trend_tabs[2]:
        st.subheader("Rata-rata Jumlah Peminjam per Kondisi Cuaca")
        fig3, ax3 = plt.subplots(figsize=(10, 5))
        weather_avg = filtered_df.groupby('weather_name')['cnt'].mean().reset_index()
        sns.barplot(x='weather_name', y='cnt', data=weather_avg, palette='Set1', ax=ax3)
        ax3.set_title('Rata-rata Jumlah Peminjam Sepeda per Kondisi Cuaca')
        ax3.set_xlabel('Kondisi Cuaca')
        ax3.set_ylabel('Rata-rata Jumlah Peminjam')
        plt.tight_layout()
        st.pyplot(fig3)
    
    # Tab 4: Berdasarkan Status Hari
    with trend_tabs[3]:
        st.subheader("Hari Kerja vs Hari Libur")
        fig4, ax4 = plt.subplots(figsize=(10, 5))
        sns.barplot(
            x='workingday', 
            y='cnt', 
            hue='workingday',
            data=filtered_df, 
            estimator=np.mean, 
            errorbar=None, 
            palette='pastel',
            ax=ax4
        )
        ax4.set_xticklabels(['Hari Libur', 'Hari Kerja'])
        ax4.set_title('Rata-rata Jumlah Peminjam Sepeda\n(Hari Kerja vs Hari Libur)')
        ax4.set_xlabel('Jenis Hari')
        ax4.set_ylabel('Rata-rata Jumlah Peminjam')
        ax4.legend([],[], frameon=False)
        plt.tight_layout()
        st.pyplot(fig4)
else:
    st.warning("Tidak ada data yang sesuai dengan filter yang dipilih.")

# Bagian kesimpulan
st.subheader("Jawaban dan Kesimpulan")
st.write("""
Berdasarkan analisis di atas:

1. **Tren Harian**: Terdapat pola musiman dalam peminjaman sepeda dengan peningkatan signifikan dari tahun 2011 ke 2012, menunjukkan pertumbuhan popularitas layanan berbagi sepeda.

2. **Faktor Musim**: Musim panas dan musim gugur memiliki rata-rata peminjaman sepeda tertinggi, sementara musim dingin menunjukkan angka terendah. Ini mengindikasikan bahwa kondisi cuaca yang lebih hangat lebih disukai untuk bersepeda.

3. **Faktor Cuaca**: Kondisi cuaca sangat mempengaruhi peminjaman sepeda di mana:
   - Cuaca cerah menghasilkan jumlah peminjaman tertinggi
   - Cuaca hujan/salju ringan dan lebat mengurangi minat bersepeda secara signifikan

4. **Faktor Hari Kerja/Libur**: Hari kerja umumnya memiliki jumlah peminjam lebih tinggi dibanding hari libur, menunjukkan bahwa sepeda banyak digunakan untuk aktivitas rutin seperti perjalanan ke tempat kerja.
""")


# Bagian Pertanyaan Analisis 2: Perbandingan pola peminjaman antara casual vs registered
st.header("Analisis Perbandingan Tipe Pengguna")

if not filtered_df.empty:
    st.subheader("Pertanyaan: Bagaimana perbandingan pola peminjaman antara pengguna casual dan registered berdasarkan hari kerja dan hari libur?")
    
    # Menggunakan tabs untuk visualisasi kedua
    user_tabs = st.tabs(["Perbandingan Pengguna", "Pola Mingguan", "Proporsi Hari Libur", "Proporsi Hari Kerja"])
    
    # Tab 1: Perbandingan Pengguna
    with user_tabs[0]:
        st.subheader("Perbandingan Pengguna Casual vs Registered")
        
        fig5, ax5 = plt.subplots(figsize=(12, 6))
        user_comparison = filtered_df.melt(
            id_vars=['workingday'],
            value_vars=['casual', 'registered'],
            var_name='User Type',
            value_name='Count'
        )
        
        sns.barplot(
            data=user_comparison,
            x='workingday',
            y='Count',
            hue='User Type',
            estimator=np.mean,
            errorbar=None,
            palette='viridis',
            ax=ax5
        )
        
        ax5.set_xticklabels(['Hari Libur', 'Hari Kerja'])
        ax5.set_title('Rata-rata Jumlah Peminjam Casual vs Registered\n(Hari Kerja vs Hari Libur)')
        ax5.set_xlabel('Jenis Hari')
        ax5.set_ylabel('Rata-rata Jumlah Peminjam')
        ax5.legend(title='Tipe Pengguna')
        plt.tight_layout()
        st.pyplot(fig5)
    
    # Tab 2: Pola Mingguan
    with user_tabs[1]:
        st.subheader("Pola Mingguan Pengguna Casual vs Registered")
        
        # Visualisasi tren pola mingguan untuk pengguna casual dan registered
        fig6, ax6 = plt.subplots(figsize=(12, 6))
        weekday_avg = filtered_df.groupby('weekday')[['casual', 'registered']].mean().reset_index()
        weekday_avg['day_name'] = weekday_avg['weekday'].apply(lambda x: ['Minggu', 'Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu'][x])
        
        ax6.plot(weekday_avg['weekday'], weekday_avg['casual'], marker='o', linewidth=2, label='Casual')
        ax6.plot(weekday_avg['weekday'], weekday_avg['registered'], marker='s', linewidth=2, label='Registered')
        ax6.set_xlabel('Hari dalam Seminggu')
        ax6.set_ylabel('Rata-rata Jumlah Peminjam')
        ax6.set_title('Pola Mingguan Peminjaman Sepeda - Casual vs Registered')
        ax6.set_xticks(range(7))
        ax6.set_xticklabels(['Minggu', 'Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu'])
        ax6.grid(alpha=0.3)
        ax6.legend()
        plt.tight_layout()
        st.pyplot(fig6)
    
    # Tab 3: Proporsi Tipe Pengguna (Hari Libur)
    with user_tabs[2]:
        st.subheader("Proporsi Tipe Pengguna (Hari Libur)")
        holiday_data = filtered_df[filtered_df['workingday'] == 0]
        if not holiday_data.empty:
            fig7, ax7 = plt.subplots(figsize=(8, 8))
            holiday_avg = holiday_data[['casual', 'registered']].mean()
            ax7.pie(
                holiday_avg, 
                labels=['Casual', 'Registered'], 
                autopct='%1.1f%%',
                startangle=90,
                colors=['#ff9999','#66b3ff']
            )
            ax7.set_title('Proporsi Pengguna pada Hari Libur')
            plt.tight_layout()
            st.pyplot(fig7)
        else:
            st.info("Tidak ada data hari libur yang tersedia dengan filter yang dipilih.")
    
    # Tab 4: Proporsi Tipe Pengguna (Hari Kerja)
    with user_tabs[3]:
        st.subheader("Proporsi Tipe Pengguna (Hari Kerja)")
        workday_data = filtered_df[filtered_df['workingday'] == 1]
        if not workday_data.empty:
            fig8, ax8 = plt.subplots(figsize=(8, 8))
            workday_avg = workday_data[['casual', 'registered']].mean()
            ax8.pie(
                workday_avg, 
                labels=['Casual', 'Registered'], 
                autopct='%1.1f%%',
                startangle=90,
                colors=['#ff9999','#66b3ff']
            )
            ax8.set_title('Proporsi Pengguna pada Hari Kerja')
            plt.tight_layout()
            st.pyplot(fig8)
        else:
            st.info("Tidak ada data hari kerja yang tersedia dengan filter yang dipilih.")
    
    # Kesimpulan analisis
    st.subheader("Jawaban dan Kesimpulan")
    st.write("""
    Berdasarkan perbandingan pola peminjaman sepeda antara pengguna casual dan registered:
    
    1. **Pengguna Casual**:
       - Lebih aktif pada hari libur dibandingkan hari kerja
       - Menunjukkan pola penggunaan yang cenderung untuk rekreasi dan aktivitas akhir pekan
    
    2. **Pengguna Registered**:
       - Jauh lebih dominan pada hari kerja
       - Menunjukkan pola yang konsisten sebagai pengguna reguler, kemungkinan menggunakan sepeda untuk kegiatan rutin seperti perjalanan ke tempat kerja
    
    3. **Implikasi Bisnis**:
       - Strategi pemasaran yang berbeda dapat diterapkan untuk kedua segmen pengguna
       - Pengguna registered merupakan basis pelanggan yang lebih stabil dan dapat menjadi target untuk program loyalitas
       - Pengguna casual memiliki potensi untuk dikonversi menjadi pengguna registered melalui promosi khusus
    """)
else:
    st.warning("Tidak ada data yang sesuai dengan filter yang dipilih.")

# Bagian Pertanyaan Analisis 3: Korelasi variabel cuaca dengan jumlah peminjaman sepeda
st.header("Analisis Pengaruh Faktor Cuaca")

if not filtered_df.empty:
    st.subheader("Pertanyaan: Bagaimana pengaruh faktor cuaca (suhu, kelembapan, kecepatan angin) terhadap jumlah peminjaman sepeda?")
        
    # Membuat tabs untuk visualisasi ketiga
    weather_tabs = st.tabs(["Korelasi", "Hubungan Faktor Cuaca"])
        
    # Tab 1: Heatmap Korelasi
    with weather_tabs[0]:
        st.subheader("Korelasi Variabel Cuaca dengan Jumlah Peminjaman")
            
        # Menghitung korelasi variabel numerik
        num_cols = ['temp', 'atemp', 'hum', 'windspeed', 'cnt']
        corr = filtered_df[num_cols].corr()
            
        fig9, ax9 = plt.subplots(figsize=(10, 8))
        sns.heatmap(corr, annot=True, cmap='coolwarm', fmt=".2f", ax=ax9)
        ax9.set_title('Heatmap Korelasi Variabel Numerik dengan Jumlah Peminjam Sepeda')
        plt.tight_layout()
        st.pyplot(fig9)
        
    # Tab 2: Scatter plots
    with weather_tabs[1]:
        st.subheader("Hubungan Faktor Cuaca dengan Jumlah Peminjaman")
            
        fig10, axs = plt.subplots(1, 3, figsize=(18, 5))
            
        sns.scatterplot(data=filtered_df, x='temp', y='cnt', ax=axs[0])
        axs[0].set_title('Suhu vs Jumlah Peminjam')
        axs[0].set_xlabel('Suhu (Normalisasi)')
        axs[0].set_ylabel('Jumlah Peminjam')
            
        sns.scatterplot(data=filtered_df, x='hum', y='cnt', ax=axs[1])
        axs[1].set_title('Kelembapan vs Jumlah Peminjam')
        axs[1].set_xlabel('Kelembapan (Normalisasi)')
        axs[1].set_ylabel('Jumlah Peminjam')
            
        sns.scatterplot(data=filtered_df, x='windspeed', y='cnt', ax=axs[2])
        axs[2].set_title('Kecepatan Angin vs Jumlah Peminjam')
        axs[2].set_xlabel('Kecepatan Angin (Normalisasi)')
        axs[2].set_ylabel('Jumlah Peminjam')
            
        plt.tight_layout()
        st.pyplot(fig10)
        
    # Kesimpulan Analisis
    st.subheader("Jawaban dan Kesimpulan")
    st.write("""
    Berdasarkan analisis pengaruh faktor cuaca terhadap jumlah peminjaman sepeda:
        
    1. **Suhu (temp, atemp)**:
        - Memiliki korelasi positif yang cukup kuat dengan jumlah peminjam sepeda
        - Semakin hangat suhu, semakin banyak peminjaman sepeda
        - Ini menunjukkan bahwa kondisi hangat lebih disukai untuk aktivitas bersepeda
        
    2. **Kelembapan (hum)**:
        - Memiliki korelasi negatif dengan jumlah peminjaman
        - Kelembapan tinggi cenderung menurunkan minat peminjaman sepeda
        - Kondisi lembab mungkin kurang nyaman untuk bersepeda
        
    3. **Kecepatan Angin (windspeed)**:
        - Juga memiliki korelasi negatif, namun lebih lemah dibanding kelembapan
        - Angin kencang dapat membuat perjalanan bersepeda lebih sulit dan kurang nyaman
        
    4. **Implikasi Bisnis**:
        - Perencanaan persediaan sepeda dapat dioptimalkan berdasarkan prediksi cuaca
        - Promosi khusus dapat dilakukan pada hari-hari dengan kondisi cuaca yang kurang ideal
        - Pertimbangan untuk menyediakan fasilitas perlindungan atau penyewaan perlengkapan tambahan pada kondisi cuaca tertentu
    """)
else:
    st.warning("Tidak ada data yang sesuai dengan filter yang dipilih.")
