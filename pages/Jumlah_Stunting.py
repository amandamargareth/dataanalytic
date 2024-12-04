import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

st.write(
        """
    # Grafik Jumlah Stunting Pada Tahun 2019-2022
        Hallo! Selamat Datang
        """
)

file_path = Path('/workspaces/dataanalytic/data/Stunting.csv')   
stunting_data = pd.read_csv(file_path)

stunting_by_year = stunting_data.groupby('tahun')['jumlah_balita_stunting'].sum().reset_index()



st.write("Berikut adalah data jumlah stunting per tahun:")
st.dataframe(stunting_by_year)

fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(stunting_by_year["tahun"], stunting_by_year["jumlah_balita_stunting"], marker="o", linestyle="-", color="red", label="Jumlah Stunting")

ax.set_title("Grafik Jumlah Stunting Tiap Tahun", fontsize=14)
ax.set_xlabel("Tahun", fontsize=12)
ax.set_ylabel("Jumlah (Orang)", fontsize=12)
ax.grid(True, linestyle="--", alpha=0.5)
ax.legend()

st.pyplot(fig)

total_reduction = stunting_by_year["jumlah_balita_stunting"].iloc[0] - stunting_by_year["jumlah_balita_stunting"].iloc[-1]
max_stunting = stunting_by_year.loc[stunting_by_year['jumlah_balita_stunting'].idxmax()]
min_stunting = stunting_by_year.loc[stunting_by_year['jumlah_balita_stunting'].idxmin()]
total_stunting = stunting_by_year["jumlah_balita_stunting"].sum()

st.write(f"**Insight:**")
st.write(f"- Dari tahun {stunting_by_year['tahun'].min()} hingga {stunting_by_year['tahun'].max()}, terjadi penurunan jumlah balita stunting sebanyak {total_reduction:,} orang.")
st.write(f"- Jumlah balita stunting terbanyak adalah Tahun **{max_stunting['tahun']}** dengan jumlah **{max_stunting['jumlah_balita_stunting']:,} orang**.")
st.write(f"- Jumlah balita stunting tersedikit adalah Tahun **{min_stunting['tahun']}** dengan jumlah **{min_stunting['jumlah_balita_stunting']:,} orang**.")
st.write(f"- Jumlah balita stunting dari 2019 hingga 2022 adalah **{total_stunting:,} orang**.")

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