import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

st.write(
    """
    # Grafik Kenaikan Jumlah Stunting Dari Tahun 2019-2022 Di Jawa Barat
    Hallo! Selamat Datang
    """
)

file_path = Path('data/Stunting.csv')  # Sesuaikan dengan lokasi file

# Debugging untuk memastikan file tersedia
if not file_path.exists():
    st.error(f"File tidak ditemukan di lokasi: {file_path.resolve()}")
else:
    try:
        # Membaca file CSV
        stunting_data = pd.read_csv(file_path)

        # Agregasi data berdasarkan tahun
        stunting_by_year = stunting_data.groupby('tahun')['jumlah_balita_stunting'].sum().reset_index()

        st.write("Berikut adalah data jumlah stunting per tahun:")
        st.dataframe(stunting_by_year)

        # Membuat grafik
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(
            stunting_by_year["tahun"],
            stunting_by_year["jumlah_balita_stunting"],
            marker="o",
            linestyle="-",
            color="red",
            label="Jumlah Stunting"
        )
        ax.set_title("Grafik Jumlah Stunting Tiap Tahun", fontsize=14)
        ax.set_xlabel("Tahun", fontsize=12)
        ax.set_ylabel("Jumlah (Orang)", fontsize=12)
        ax.grid(True, linestyle="--", alpha=0.5)
        ax.legend()
        st.pyplot(fig)

        # Insight tambahan
        total_reduction = stunting_by_year["jumlah_balita_stunting"].iloc[0] - stunting_by_year["jumlah_balita_stunting"].iloc[-1]
        max_stunting = stunting_by_year.loc[stunting_by_year['jumlah_balita_stunting'].idxmax()]
        min_stunting = stunting_by_year.loc[stunting_by_year['jumlah_balita_stunting'].idxmin()]
        total_stunting = stunting_by_year["jumlah_balita_stunting"].sum()

        st.write(f"**Insight:**")
        st.write(f"- Dari tahun {stunting_by_year['tahun'].min()} hingga {stunting_by_year['tahun'].max()}, terjadi penurunan jumlah balita stunting sebanyak {total_reduction:,} orang.")
        st.write(f"- Jumlah balita stunting terbanyak adalah Tahun **{max_stunting['tahun']}** dengan jumlah **{max_stunting['jumlah_balita_stunting']:,} orang**.")
        st.write(f"- Jumlah balita stunting tersedikit adalah Tahun **{min_stunting['tahun']}** dengan jumlah **{min_stunting['jumlah_balita_stunting']:,} orang**.")
        st.write(f"- Jumlah balita stunting dari 2019 hingga 2022 adalah **{total_stunting:,} orang**.")
    except Exception as e:
        st.error(f"Terjadi kesalahan saat memproses file: {e}")


import streamlit as st
import pandas as pd
import altair as alt

st.title("Grafik Jumlah Stunting di Tiap Kota")
file_path = "data/Stunting.csv"  # Nama file CSV

try:
    # Membaca file CSV
    df = pd.read_csv(file_path, thousands=",")

    # Memastikan kolom yang diperlukan ada
    required_columns = ['nama_kabupaten_kota', 'tahun', 'jumlah_balita_stunting']
    if all(col in df.columns for col in required_columns):
        # Filter hanya kolom yang dibutuhkan
        df_display = df[required_columns]
        st.subheader("Data Jumlah Stunting")
        st.dataframe(df_display)

        # Menampilkan grafik bar dengan Altair
        st.subheader("Grafik Jumlah Stunting disetiap kabupaten/kota di Jawa Barat")
        chart = (
            alt.Chart(df_display)
            .mark_bar()
            .encode(
                x=alt.X("nama_kabupaten_kota", sort="-y", title="Nama Kabupaten/Kota"),
                y=alt.Y("jumlah_balita_stunting", title="Jumlah Balita Stunting (orang)"),
                color=alt.Color("tahun:N", title="Tahun", legend=alt.Legend(orient="top")),
                tooltip=["nama_kabupaten_kota", "tahun", "jumlah_balita_stunting"]
            )
            .properties(width=800, height=400)
        )
        st.altair_chart(chart, use_container_width=True)

        # Rangkuman Insight
        st.subheader("Insight")
        st.markdown("""
        1. **Kabupaten Bogor** memiliki jumlah stunting tertinggi dibandingkan kabupaten/kota lainnya di Jawa Barat.
        2. **Kota Banjar** memiliki jumlah kasus stunting yang paling rendah secara konsisten.
        3. Tren per tahun menunjukkan beberapa daerah mengalami penurunan kasus stunting, namun tidak merata di semua wilayah.
        """)
    else:
        st.error("File CSV tidak memiliki kolom yang dibutuhkan: 'nama_kabupaten_kota', 'tahun', 'jumlah_balita_stunting'.")
except FileNotFoundError:
    st.error(f"File '{file_path}' tidak ditemukan. Pastikan file berada di lokasi yang benar.")
except Exception as e:
    st.error(f"Terjadi kesalahan: {e}")

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Path ke file CSV
file_path = "data/Stunting.csv" 

try:
    # Membaca file CSV dan hanya memilih kolom yang relevan
    df = pd.read_csv(file_path, thousands=",")[['nama_kabupaten_kota', 'jumlah_balita_stunting', 'tahun']]

    st.title("Analisis Jumlah Stunting per Kabupaten/Kota")

    # Dropdown untuk memilih tahun
    tahun = st.selectbox("Pilih Tahun:", options=sorted(df['tahun'].unique()), index=0)

    # Filter data berdasarkan tahun yang dipilih
    filtered_df = df[df['tahun'] == tahun]

    # Menampilkan data dalam tabel
    st.subheader(f"Data Jumlah Stunting untuk Tahun {tahun}:")
    st.dataframe(filtered_df.style.format({'jumlah_balita_stunting': '{:.0f}'}))

    # Grafik batang menggunakan Matplotlib
    st.subheader(f"Grafik Jumlah Stunting per Kabupaten/Kota - {tahun}")
    plt.figure(figsize=(10, 6))
    plt.bar(filtered_df['nama_kabupaten_kota'], filtered_df['jumlah_balita_stunting'], color='skyblue')
    plt.title(f"Grafik Jumlah Stunting per Kabupaten/Kota - {tahun}", fontsize=14)
    plt.xlabel("Kabupaten/Kota", fontsize=12)
    plt.ylabel("Jumlah Balita Stunting", fontsize=12)
    plt.xticks(rotation=45, ha='right')
    st.pyplot(plt)

# Total jumlah stunting untuk tahun yang dipilih
    total_stunting = filtered_df['jumlah_balita_stunting'].sum()
    st.markdown(f"**Total jumlah stunting pada tahun {tahun}: {total_stunting:.0f} orang.**")

    # Insight: Kota/Kabupaten dengan stunting terbanyak dan tersedikit
    terbanyak = filtered_df.loc[filtered_df['jumlah_balita_stunting'].idxmax()]
    tersedikit = filtered_df.loc[filtered_df['jumlah_balita_stunting'].idxmin()]
    st.subheader("Insight")
    st.markdown(
        f"1. Kota/Kabupaten dengan jumlah stunting **terbanyak** adalah "
        f"**{terbanyak['nama_kabupaten_kota']}** dengan jumlah **{terbanyak['jumlah_balita_stunting']:.0f} orang**."
    )
    st.markdown(
        f"2. Kota/Kabupaten dengan jumlah stunting **tersedikit** adalah "
        f"**{tersedikit['nama_kabupaten_kota']}** dengan jumlah **{tersedikit['jumlah_balita_stunting']:.0f} orang**."
    )
except FileNotFoundError:
    st.error(f"File '{file_path}' tidak ditemukan. Pastikan file berada di lokasi yang benar.")
except Exception as e:
    st.error(f"Terjadi kesalahan: {e}")
