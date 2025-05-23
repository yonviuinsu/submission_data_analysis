import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import os
import matplotlib.pyplot as plt

# Mengatur judul halaman dan konfigurasi
st.set_page_config(
    page_title="Dashboard Berbagi Sepeda",
    layout="wide"
)

# Judul dashboard
st.title("Dashboard Analisis Berbagi Sepeda")

# Memuat dataset (sesuaikan path ke lokasi dataset yang telah diproses)
@st.cache_data
def load_data():
    # Membaca file CSV
    day_df = pd.read_csv('dashboard/day.csv')
    # Mengubah kolom tanggal ke format datetime
    day_df['date'] = pd.to_datetime(day_df['dteday'])
    return day_df

# Memuat data
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

# Bagian Pertanyaan Analisis 5: Analisis Segmentasi dan Perilaku Pengguna
st.header("Analisis Segmentasi dan Perilaku Pengguna")

if not filtered_df.empty:
    st.subheader("Pertanyaan: Bagaimana segmentasi pengguna berdasarkan rasio casual vs registered dan bagaimana perilaku mereka berbeda?")
    
    # Menambahkan kolom rasio untuk analisis
    day_df['casual_ratio'] = day_df['casual'] / day_df['cnt']
    day_df['registered_ratio'] = day_df['registered'] / day_df['cnt']
    
    # Membuat tabs untuk visualisasi kelima
    segment_tabs = st.tabs(["Distribusi Rasio", "Pola Musiman", "Elastisitas Cuaca", "Volatilitas"])
    
    # Tab 1: Distribusi dan Tren Rasio
    with segment_tabs[0]:
        st.subheader("Distribusi dan Tren Rasio Pengguna")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Visualisasi distribusi rasio pengguna casual
            fig14, ax14 = plt.subplots(figsize=(6, 4))
            sns.histplot(day_df['casual_ratio'], kde=True, bins=20, color='skyblue', ax=ax14)
            ax14.set_title('Distribusi Rasio Pengguna Casual')
            ax14.set_xlabel('Rasio Pengguna Casual (casual/total)')
            ax14.set_ylabel('Frekuensi')
            plt.tight_layout()
            st.pyplot(fig14)
        
        with col2:
            # Visualisasi perubahan rasio pengguna casual dari waktu ke waktu
            fig15, ax15 = plt.subplots(figsize=(6, 4))
            sns.lineplot(data=day_df, x='date', y='casual_ratio', color='coral', ax=ax15)
            ax15.set_title('Tren Rasio Pengguna Casual Sepanjang Waktu')
            ax15.set_xlabel('Tanggal')
            ax15.set_ylabel('Rasio Pengguna Casual')
            plt.tight_layout()
            st.pyplot(fig15)
    
    # Tab 2: Pola Musiman Segmen Pengguna
    with segment_tabs[1]:
        st.subheader("Pola Peminjaman Berdasarkan Musim dan Jenis Hari")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Pola peminjaman pengguna casual
            seasonal_casual = day_df.groupby(['season', 'workingday'])['casual'].mean().reset_index()
            seasonal_casual_pivot = seasonal_casual.pivot(index='season', columns='workingday', values='casual')
            
            fig16, ax16 = plt.subplots(figsize=(6, 5))
            sns.heatmap(seasonal_casual_pivot, annot=True, cmap='YlGnBu', fmt='.1f', ax=ax16)
            ax16.set_title('Rata-rata Peminjaman Pengguna Casual\nBerdasarkan Musim dan Jenis Hari')
            ax16.set_xlabel('Jenis Hari (0: Libur, 1: Kerja)')
            ax16.set_ylabel('Musim (1: Semi, 2: Panas, 3: Gugur, 4: Dingin)')
            plt.tight_layout()
            st.pyplot(fig16)
        
        with col2:
            # Pola peminjaman pengguna registered
            seasonal_registered = day_df.groupby(['season', 'workingday'])['registered'].mean().reset_index()
            seasonal_registered_pivot = seasonal_registered.pivot(index='season', columns='workingday', values='registered')
            
            fig17, ax17 = plt.subplots(figsize=(6, 5))
            sns.heatmap(seasonal_registered_pivot, annot=True, cmap='YlOrRd', fmt='.1f', ax=ax17)
            ax17.set_title('Rata-rata Peminjaman Pengguna Registered\nBerdasarkan Musim dan Jenis Hari')
            ax17.set_xlabel('Jenis Hari (0: Libur, 1: Kerja)')
            ax17.set_ylabel('Musim (1: Semi, 2: Panas, 3: Gugur, 4: Dingin)')
            plt.tight_layout()
            st.pyplot(fig17)
    
    # Tab 3: Elastisitas terhadap Cuaca
    with segment_tabs[2]:
        st.subheader("Elastisitas Permintaan terhadap Kondisi Cuaca")
        
        # Analisis elastisitas permintaan terhadap kondisi cuaca
        weather_elasticity = day_df.groupby(['weathersit'])[['casual', 'registered', 'cnt']].mean()
        
        fig18, ax18 = plt.subplots(figsize=(10, 6))
        weather_elasticity.plot(kind='bar', ax=ax18)
        ax18.set_title('Pengaruh Kondisi Cuaca terhadap Jumlah Peminjaman')
        ax18.set_xlabel('Kondisi Cuaca (1: Cerah, 2: Mendung, 3: Hujan)')
        ax18.set_ylabel('Rata-rata Jumlah Peminjaman')
        ax18.set_xticklabels(['Cerah', 'Mendung', 'Hujan'], rotation=0)
        ax18.legend(['Casual', 'Registered', 'Total'])
        ax18.grid(axis='y', alpha=0.3)
        plt.tight_layout()
        st.pyplot(fig18)
        
        # Menghitung persentase perubahan
        weather_pct_change = weather_elasticity.pct_change() * 100
        st.write("Persentase Perubahan Peminjaman saat Perubahan Kondisi Cuaca:")
        st.dataframe(weather_pct_change.round(2))
    
    # Tab 4: Volatilitas Peminjaman
    with segment_tabs[3]:
        st.subheader("Volatilitas Peminjaman Sepeda per Bulan")
        
        # Identifikasi pola variabilitas harian
        day_df['month_year'] = day_df['date'].dt.to_period('M')
        monthly_volatility = day_df.groupby('month_year')['cnt'].agg(['mean', 'std'])
        monthly_volatility['cv'] = monthly_volatility['std'] / monthly_volatility['mean'] * 100  # Coefficient of variation
        
        fig19, ax19 = plt.subplots(figsize=(12, 6))
        ax19.bar(monthly_volatility.index.astype(str), monthly_volatility['cv'], color='teal')
        ax19.set_title('Volatilitas Peminjaman Sepeda per Bulan (Coefficient of Variation)')
        ax19.set_xlabel('Bulan')
        ax19.set_ylabel('Coefficient of Variation (%)')
        plt.xticks(rotation=45)
        ax19.grid(axis='y', alpha=0.3)
        plt.tight_layout()
        st.pyplot(fig19)
    
    # Kesimpulan dan Rekomendasi
    st.subheader("Insight dan Rekomendasi Strategis")
    st.write("""
    **Insight Segmentasi Pengguna:**

    1. **Segmentasi Pengguna:**
        - Rasio pengguna casual terhadap total peminjam bervariasi secara signifikan, dengan rata-rata sekitar 30-35%.
        - Terdapat pola musiman yang jelas pada rasio pengguna casual, dimana proporsi pengguna casual meningkat pada musim panas dan akhir pekan.
        - Strategi pemasaran yang berbeda dapat diterapkan untuk kedua segmen pengguna ini dengan mempertimbangkan pola penggunaan mereka yang berbeda.

    2. **Perbedaan Perilaku Pengguna berdasarkan Musim:**
        - Pengguna casual sangat dipengaruhi oleh musim, dengan peminjaman tertinggi pada musim panas dan akhir pekan.
        - Pengguna registered lebih stabil sepanjang tahun namun tetap menunjukkan variasi musiman dengan puncak pada musim panas/gugur pada hari kerja.
        - Pengguna casual menunjukkan penurunan drastis pada kondisi cuaca buruk, sementara pengguna registered lebih tahan terhadap perubahan cuaca.

    3. **Elastisitas terhadap Cuaca:**
        - Permintaan pengguna casual lebih elastis terhadap perubahan kondisi cuaca dibanding pengguna registered.
        - Transisi dari cuaca cerah ke mendung menurunkan permintaan casual secara signifikan, sedangkan dari mendung ke hujan menurunkan permintaan lebih drastis lagi.
        - Informasi ini dapat digunakan untuk menyesuaikan distribusi sepeda dan strategi promosi berdasarkan prakiraan cuaca.

    4. **Volatilitas Penggunaan:**
        - Bulan-bulan musim dingin menunjukkan volatilitas peminjaman sepeda yang lebih tinggi, menandakan ketidakpastian penggunaan yang lebih besar.
        - Bulan-bulan dengan volatilitas tinggi memerlukan perencanaan operasional yang lebih fleksibel untuk mengakomodasi fluktuasi permintaan yang lebih besar.
        - Pemahaman tentang volatilitas ini dapat membantu optimalisasi alokasi sumber daya dan perencanaan pemeliharaan armada sepeda.

    **Rekomendasi Strategis:**
    - Kembangkan program insentif khusus untuk meningkatkan penggunaan pada cuaca buruk, terutama ditargetkan pada pengguna registered yang lebih stabil.
    - Desain paket berlangganan fleksibel untuk mengkonversi pengguna casual menjadi pengguna registered untuk meningkatkan stabilitas penggunaan.
    - Terapkan sistem prediksi permintaan berbasis cuaca untuk mengoptimalkan distribusi sepeda.
    - Pertimbangkan strategi penetapan harga dinamis berdasarkan musim dan kondisi cuaca untuk memaksimalkan pendapatan dan distribusi penggunaan.
    """)
else:
    st.warning("Tidak ada data yang sesuai dengan filter yang dipilih.")
