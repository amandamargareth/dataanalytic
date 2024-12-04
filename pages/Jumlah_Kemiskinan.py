import streamlit as st
import pandas as pd
from pathlib import Path

st.title("Jumlah Kemiskinan Di Indonesia")


# Fungsi untuk membaca data jumlah kemiskinan
@st.cache_data
def get_poverty_data():
    DATA_1 = Path(__file__).parent / 'data/Jumlah_Kemiskinan.csv'
    poverty_df = pd.read_csv(DATA_1)

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
st.write("Tabel Jumlah Kemiskinan Penduduk:", filtered_poverty_df)

# Cek jika data kosong
if filtered_poverty_df.empty:
    st.warning("No data available for the selected year range.")
else:
    # Pastikan data numerik
    filtered_poverty_df['tahun'] = pd.to_numeric(filtered_poverty_df['tahun'], errors='coerce')
    filtered_poverty_df['jumlah_penduduk_miskin'] = pd.to_numeric(filtered_poverty_df['jumlah_penduduk_miskin'], errors='coerce')
    filtered_poverty_df = filtered_poverty_df.dropna(subset=['tahun', 'jumlah_penduduk_miskin'])

    # Menghitung total jumlah penduduk miskin per tahun
    total_poverty_per_year = filtered_poverty_df.groupby('tahun')['jumlah_penduduk_miskin'].sum().reset_index()

    # Grafik batang (Bar Chart)
    st.write("Grafik Jumlah Data Kemiskinan Pada Tahun 2019-2022")
    st.bar_chart(
        total_poverty_per_year.set_index('tahun')['jumlah_penduduk_miskin']
    )

    with st.expander("Penjelasan"):
        st.write("Berdasarkan grafik tersebut, dapat disimpulkan bahwa jumlah penduduk miskin di Indonesia cenderung mengalami peningkatan, terutama pada periode tahun 2019 hingga 2021, kemudian menunjukkan penurunan pada tahun 2022.")
