import streamlit as st
import pandas as pd
from pathlib import Path

st.title("Jumlah Kemiskinan Di Jawa Barat")

@st.cache_data
def get_poverty_data():
    DATA_1 = Path('data/Jumlah_Kemiskinan.csv')
    try:
        # Periksa apakah file ada
        if not DATA_1.exists():
            st.error(f"File {DATA_1} tidak ditemukan. Pastikan file tersedia.")
            return pd.DataFrame()  # Return DataFrame kosong
        
        # Membaca file CSV
        poverty_df = pd.read_csv(DATA_1)

        # Filter data untuk tahun 2019-2022
        poverty_df = poverty_df[(poverty_df['tahun'] >= 2019) & (poverty_df['tahun'] <= 2022)]
        return poverty_df

    except Exception as e:
        st.error(f"Terjadi kesalahan saat membaca file: {e}")
        return pd.DataFrame()

# Load data jumlah kemiskinan
poverty_df = get_poverty_data()

if poverty_df.empty:
    st.warning("Data tidak tersedia atau file tidak ditemukan.")
else:
    # Slider untuk filter tahun
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


import streamlit as st
import pandas as pd
import altair as alt
from pathlib import Path

# Load CSV File
uploaded_file = "data/Jumlah_Kemiskinan.csv"  # Nama file
df = pd.read_csv(uploaded_file)

# Filter columns to display only relevant data
df_display = df[['nama_kabupaten_kota', 'tahun', 'jumlah_penduduk_miskin']]

# Title
st.title("Grafik Jumlah Kemiskinan tiap Kota/Kabupaten Di Jawa Barat")

# Data Table
st.subheader("Data jumlah kemiskinan tiap Kota/Kabupaten pada periode 2019-2022")
st.dataframe(df_display)

# Altair Bar Chart
bar_chart = alt.Chart(df_display).mark_bar().encode(
    x=alt.X('nama_kabupaten_kota:N', title="Nama Kabupaten/Kota", sort='-y'),
    y=alt.Y('jumlah_penduduk_miskin:Q', title="Jumlah Penduduk Miskin"),
    color=alt.Color('tahun:N', legend=alt.Legend(title="Tahun")),
    tooltip=[
        alt.Tooltip('nama_kabupaten_kota:N', title="Kabupaten/Kota"),
        alt.Tooltip('tahun:N', title="Tahun"),
        alt.Tooltip('jumlah_penduduk_miskin:Q', title="Jumlah Penduduk Miskin", format=",")
    ]
).properties(
    width=800,
    height=400,
    title="Grafik Jumlah Kemiskinan per Kota/Kabupaten"
).configure_axis(
    labelAngle=-45
)

# Display Chart
st.altair_chart(bar_chart, use_container_width=True)

# Insight Section
st.header("Insight")

# Kesimpulan: Kabupaten/Kota dengan Kemiskinan Tertinggi di Setiap Tahun
st.subheader("Kabupaten/Kota dengan Jumlah Kemiskinan Tertinggi per Tahun")
top_per_year = df_display.loc[df_display.groupby('tahun')['jumlah_penduduk_miskin'].idxmax()]
for _, row in top_per_year.iterrows():
    st.write(f"Tahun *{row['tahun']}: *{row['nama_kabupaten_kota']}* dengan jumlah penduduk miskin *{int(row['jumlah_penduduk_miskin']):,}**.")

# Kesimpulan: Kabupaten/Kota dengan Total Kemiskinan Tertinggi (2019-2022)
st.subheader("Kabupaten/Kota dengan Total Kemiskinan Tertinggi (2019-2022)")
total_kemiskinan = df_display.groupby('nama_kabupaten_kota')['jumlah_penduduk_miskin'].sum().reset_index()
top_total = total_kemiskinan.loc[total_kemiskinan['jumlah_penduduk_miskin'].idxmax()]
st.write(f"Secara total selama periode 2019-2022, kabupaten/kota dengan jumlah kemiskinan tertinggi adalah *{top_total['nama_kabupaten_kota']}* dengan total penduduk miskin sebanyak *{int(top_total['jumlah_penduduk_miskin']):,}*.")