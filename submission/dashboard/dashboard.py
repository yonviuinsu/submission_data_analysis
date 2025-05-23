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




# Bagian Pertanyaan Analisis 4: Analisis tren musiman dan pertumbuhan tahunan
st.header("Analisis Tren Musiman dan Pertumbuhan Tahunan")

# Tambahkan kolom untuk keperluan analisis
day_df['year'] = day_df['date'].dt.year - 2011  # 0 untuk 2011, 1 untuk 2012
day_df['month'] = day_df['date'].dt.month
day_df['total_count'] = day_df['cnt']  # Menggunakan total count untuk analisis

st.subheader("Pertanyaan: Bagaimana pola tren musiman dan pertumbuhan tahunan peminjaman sepeda selama periode 2011-2012?")

# Membuat tabs untuk visualisasi keempat
trend_tabs = st.tabs(["Tren Bulanan", "Perbandingan Kuartal", "Pola Mingguan"])

# Tab 1: Tren Bulanan
with trend_tabs[0]:
    st.subheader("Tren Musiman Peminjaman Sepeda per Bulan")
    
    # Visualisasi tren musiman per bulan
    fig11, ax11 = plt.subplots(figsize=(12, 6))
    monthly_data = day_df.groupby(['year', 'month'])['total_count'].mean().reset_index()
    month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    monthly_data['month_name'] = monthly_data['month'].apply(lambda x: month_names[x-1])

    # Plot untuk setiap tahun
    for year in [0, 1]:  # Tahun 2011 (0) dan 2012 (1)
        year_data = monthly_data[monthly_data['year'] == year]
        ax11.plot(year_data['month'], year_data['total_count'], 
                marker='o', 
                linewidth=2, 
                label=f'Tahun {year+2011}')
    
    ax11.set_xlabel('Bulan')
    ax11.set_ylabel('Rata-rata Jumlah Peminjam')
    ax11.set_title('Tren Musiman Peminjaman Sepeda per Bulan (2011-2012)')
    ax11.set_xticks(range(1, 13))
    ax11.set_xticklabels(month_names)
    ax11.grid(alpha=0.3)
    ax11.legend()
    plt.tight_layout()
    st.pyplot(fig11)

# Tab 2: Perbandingan Kuartal
with trend_tabs[1]:
    st.subheader("Perbandingan Rata-rata Peminjaman per Kuartal")
    
    # Visualisasi tren jangka panjang: perbandingan kuartal antar tahun
    fig12, ax12 = plt.subplots(figsize=(10, 6))
    day_df['quarter'] = ((day_df['month']-1) // 3) + 1
    quarterly_data = day_df.groupby(['year', 'quarter'])['total_count'].mean().reset_index()

    sns.barplot(x='quarter', y='total_count', hue='year', 
              palette=['skyblue', 'orange'],
              data=quarterly_data, ax=ax12)
    ax12.set_xlabel('Kuartal')
    ax12.set_ylabel('Rata-rata Jumlah Peminjam')
    ax12.set_title('Perbandingan Rata-rata Peminjaman Sepeda per Kuartal (2011 vs 2012)')
    ax12.set_xticks([0, 1, 2, 3])
    ax12.set_xticklabels(['Q1 (Jan-Mar)', 'Q2 (Apr-Jun)', 'Q3 (Jul-Sep)', 'Q4 (Oct-Dec)'])
    ax12.legend(title='Tahun', labels=['2011', '2012'])
    ax12.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    st.pyplot(fig12)

# Tab 3: Pola Mingguan
with trend_tabs[2]:
    st.subheader("Perbandingan Pola Mingguan Antar Tahun")
    
    # Visualisasi perbandingan hari dalam seminggu antara tahun 2011 dan 2012
    fig13, ax13 = plt.subplots(figsize=(12, 6))
    weekday_data = day_df.groupby(['year', 'weekday'])['total_count'].mean().reset_index()
    day_names = ['Minggu', 'Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu']
    weekday_data['day_name'] = weekday_data['weekday'].apply(lambda x: day_names[x])

    sns.lineplot(data=weekday_data, x='weekday', y='total_count', hue='year', 
               marker='o', markersize=10, linewidth=2,
               palette=['skyblue', 'orange'], ax=ax13)
    ax13.set_xlabel('Hari dalam Seminggu')
    ax13.set_ylabel('Rata-rata Jumlah Peminjam')
    ax13.set_title('Perbandingan Pola Mingguan Peminjaman Sepeda (2011 vs 2012)')
    ax13.set_xticks(range(7))
    ax13.set_xticklabels(day_names)
    ax13.legend(title='Tahun', labels=['2011', '2012'])
    ax13.grid(alpha=0.3)
    plt.tight_layout()
    st.pyplot(fig13)

# Kesimpulan Analisis
st.subheader("Jawaban dan Kesimpulan")
st.write("""
**Berdasarkan analisis tren musiman dan pertumbuhan tahunan:**

- **Tren Musiman**: Grafik bulanan menunjukkan pola musiman yang konsisten selama dua tahun berturut-turut, dengan peminjaman terendah di bulan-bulan musim dingin (Desember-Februari) dan tertinggi di bulan-bulan musim panas (Juni-September). Pola ini sangat konsisten dan dapat diprediksi.

- **Pertumbuhan Tahunan**: Data menunjukkan tren pertumbuhan yang jelas dari 2011 ke 2012 di semua bulan, dengan rata-rata peningkatan sekitar 50-70%. Pertumbuhan ini menandakan bahwa popularitas layanan bike sharing meningkat signifikan.

- **Perbandingan Kuartal**: Visualisasi kuartal dengan jelas menunjukkan bahwa Q2 (Apr-Jun) dan Q3 (Jul-Sep) secara konsisten menjadi periode puncak peminjaman sepeda, sementara Q1 (Jan-Mar) selalu menjadi periode terendah.

- **Pola Mingguan**: Terdapat pola peminjaman mingguan yang konsisten antara 2011 dan 2012, dengan Selasa hingga Jumat menjadi hari-hari dengan peminjaman tertinggi, sementara akhir pekan menunjukkan penurunan, terutama pada hari Minggu.

**Implikasi untuk Perencanaan Operasional dan Promosi:**
- Distribusi armada sepeda perlu ditingkatkan selama musim panas (Q2-Q3) untuk mengantisipasi lonjakan permintaan
- Promosi dan insentif khusus dapat diberikan selama musim dingin (Q1 dan Q4) untuk menjaga tingkat penggunaan
- Perawatan armada dapat dijadwalkan selama periode penggunaan rendah di bulan-bulan musim dingin
- Promosi akhir pekan dapat dirancang untuk meningkatkan penggunaan pada hari Sabtu-Minggu yang cenderung lebih rendah
- Persiapan ekspansi layanan perlu dilakukan mengingat tren pertumbuhan yang konsisten dari tahun ke tahun
""")
