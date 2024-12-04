import streamlit as st
import pandas as pd
from pathlib import Path

st.title("Jumlah Balita Stunting Di Indonesia")


# Fungsi untuk membaca data jumlah kemiskinan
@st.cache_data
def get_poverty_data():
    DATA_2 = Path('/workspaces/dataanalytic/data/Stunting.csv')
    poverty_df = pd.read_csv(DATA_2)

    # Filter data untuk tahun 2019-2022
    poverty_df = poverty_df[(poverty_df['tahun'] >= 2019) & (poverty_df['tahun'] <= 2022)]
    return poverty_df

# Load data jumlah kemiskinan
poverty_df = get_poverty_data()


# Filter tahun
from_year, to_year = st.slider(
    "Select year range:",
    min_value=2019,
    max_value=2022,
    value=(2019, 2022),
)

# Filter data berdasarkan tahun
filtered_poverty_df = poverty_df[
    (poverty_df['tahun'] >= from_year) & (poverty_df['tahun'] <= to_year)
]

# Debugging: Tampilkan data
st.write("Tabel Jumlah Balita Stunting:", filtered_poverty_df)

# Cek jika data kosong
if filtered_poverty_df.empty:
    st.warning("No data available for the selected year range.")
else:
    # Pastikan data numerik
    filtered_poverty_df['tahun'] = pd.to_numeric(filtered_poverty_df['tahun'], errors='coerce')
    filtered_poverty_df['jumlah_balita_stunting'] = pd.to_numeric(filtered_poverty_df['jumlah_balita_stunting'], errors='coerce')
    filtered_poverty_df = filtered_poverty_df.dropna(subset=['tahun', 'jumlah_balita_stunting'])

    # Menghitung total jumlah penduduk miskin per tahun
    total_poverty_per_year = filtered_poverty_df.groupby('tahun')['jumlah_balita_stunting'].sum().reset_index()

    # Grafik batang (Bar Chart)
    st.write("Grafik Jumlah Data Balita Stunting Pada Tahun 2019-2022")
    st.bar_chart(
        total_poverty_per_year.set_index('tahun')['jumlah_balita_stunting']
    )

    with st.expander("Penjelasan"):
        st.write("Berdasarkan grafik tersebut, dapat disimpulkan bahwa jumlah penduduk miskin di Indonesia cenderung mengalami peningkatan, terutama pada periode tahun 2019 hingga 2021, kemudian menunjukkan penurunan pada tahun 2022.")

st.title("Grafik Jumlah Stunting di Tiap Kota")
file_path = Path('/workspaces/dataanalytic/data/Stunting.csv') 
try:
    # Membaca file CSV
    df = pd.read_csv(file_path, thousands=",")
    
    # Menghapus kolom yang tidak perlu
    if 'tahun' in df.columns:
        df = df.drop(columns=['tahun'])
    if 'file' in df.columns:
        df = df.drop(columns=['file'])
    
    # Mengecek jika kolom 'nama_kabupaten_kota' dan 'jumlah_stunting' ada di dataframe
    if "nama_kabupaten_kota" in df.columns and "jumlah_balita_stunting" in df.columns:
        st.subheader("Data Jumlah Stunting")
        
        # Menampilkan data jumlah stunting hanya untuk setiap kabupaten/kota
        st.dataframe(df[['nama_kabupaten_kota', 'jumlah_balita_stunting']])
        
        # Menampilkan grafik bar jumlah stunting
        st.subheader("Grafik Bar Jumlah Stunting")
        st.bar_chart(df.set_index("nama_kabupaten_kota")["jumlah_balita_stunting"])
    else:
        st.error("Kolom 'nama_kabupaten_kota' atau 'jumlah_balita_stunting' tidak ditemukan di file CSV.")
except FileNotFoundError:
    st.error(f"File '{file_path}' tidak ditemukan. Pastikan file berada di lokasi yang benar.")
except Exception as e:
    st.error(f"Terjadi kesalahan: {e}")