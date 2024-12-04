import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Judul aplikasi
st.title("Analisis Hubungan Antara Kemiskinan dan Stunting di Jawa Barat")

# Display nama-nama pembuat
st.markdown("""
    <div style="text-align: center;">
        Disusun oleh:
    </div>
    """, 
    unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.header("Annisa")
    st.image("https://via.placeholder.com/150", use_container_width=True)
    if st.button('NRP Annisa'):
        st.write('220534024')

with col2:
    st.header("Amanda")
    st.image("https://via.placeholder.com/150", use_container_width=True)
    if st.button('NRP Amanda'):
        st.write('220534025')

with col3:
    st.header("Widya")
    st.image("https://via.placeholder.com/150", use_container_width=True)
    if st.button('NRP Widya'):
        st.write('220534026')

with col4:
    st.header("Noviyanti")
    st.image("https://via.placeholder.com/150", use_container_width=True)
    if st.button('NRP Novi'):
        st.write('220534028')

# Global file paths
DATA_1 = Path('data/Jumlah_Kemiskinan.csv')
DATA_2 = Path('data/Stunting.csv')

# Check if files exist
if not DATA_1.exists():
    st.error(f"File {DATA_1} tidak ditemukan. Pastikan file tersedia di direktori yang benar.")
elif not DATA_2.exists():
    st.error(f"File {DATA_2} tidak ditemukan. Pastikan file tersedia di direktori yang benar.")
else:
    # Fungsi untuk membaca data jumlah kemiskinan dan stunting
    @st.cache_data
    def get_combined_data():
        # Membaca data
        poverty_df = pd.read_csv(DATA_1)
        stunting_df = pd.read_csv(DATA_2)

        # Filter data untuk tahun 2019-2022
        poverty_df = poverty_df[(poverty_df['tahun'] >= 2019) & (poverty_df['tahun'] <= 2022)]
        stunting_df = stunting_df[(stunting_df['tahun'] >= 2019) & (stunting_df['tahun'] <= 2022)]

        # Menggabungkan data berdasarkan kolom 'tahun'
        combined_df = pd.merge(poverty_df, stunting_df, on='tahun', how='inner')

        return combined_df

    # Load combined data
    combined_df = get_combined_data()

    # Menjumlahkan jumlah penduduk miskin dan stunting per tahun
    summed_data = combined_df.groupby('tahun')[['jumlah_penduduk_miskin', 'jumlah_balita_stunting']].sum().reset_index()

    # Tampilkan data gabungan (hanya kolom yang diperlukan)
    st.write("Data Gabungan (Jumlah per Tahun):")
    st.dataframe(summed_data)

    # Plot grafik batang
    st.write("Grafik Perbandingan Jumlah Penduduk Miskin dan Stunting (2019-2022)")
    fig, ax = plt.subplots(figsize=(10, 6))
    x = summed_data['tahun']
    bar_width = 0.4

    # Bar data penduduk miskin
    ax.bar(x - bar_width / 2, summed_data['jumlah_penduduk_miskin'], bar_width, label='Penduduk Miskin', color='skyblue')

    # Bar data penduduk stunting
    ax.bar(x + bar_width / 2, summed_data['jumlah_balita_stunting'], bar_width, label='Penduduk Stunting', color='pink')

    # Menambahkan label dan judul
    ax.set_xlabel('Tahun')
    ax.set_ylabel('Jumlah (dalam ribuan/miliar)')
    ax.set_title('Grafik Perbandingan Penduduk Miskin dan Stunting (2019-2022)')
    ax.set_xticks(x)
    ax.legend()

    # Tampilkan grafik di Streamlit
    st.pyplot(fig)
