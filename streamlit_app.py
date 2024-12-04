import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

st.title("Analisis Hubungan Antara Kemiskinan dan Stunting di Indonesia")

st.markdown("""
    <div style="text-align: center;">
        Disusun oleh :
    </div>
    """, 
    unsafe_allow_html=True)
col1,col2,col3,col4 = st.columns(4)

with col1 :
    st.header("Annisa")
    st.image("https://scontent.fbdo9-1.fna.fbcdn.net/v/t39.30808-6/468405109_122190413258168129_1314148763243046065_n.jpg?_nc_cat=110&ccb=1-7&_nc_sid=833d8c&_nc_ohc=O-4oiEGm_jkQ7kNvgHUvoJT&_nc_zt=23&_nc_ht=scontent.fbdo9-1.fna&_nc_gid=Ay4S3WJLlTlymBkUOjPezj4&oh=00_AYDAsksbR7YOAFzWhVp6vTboT4qtJeXe41HaUj6eJJkGyg&oe=6755CBD7", use_container_width=True)
    if st.button('NRP Annisa'):
        st.write('220534024')    

with col2 :
    st.header("Amanda")
    st.image("https://scontent.fbdo9-1.fna.fbcdn.net/v/t39.30808-6/468281884_122190412982168129_542957181432111322_n.jpg?_nc_cat=102&ccb=1-7&_nc_sid=833d8c&_nc_ohc=SkeBdY_hbbMQ7kNvgH1xlm7&_nc_zt=23&_nc_ht=scontent.fbdo9-1.fna&_nc_gid=Ag11E5JXrrd7QC2x98GGADE&oh=00_AYAdxI8AVK_NTFfQW8Vic5Y790_AWQ6MfhlD3eUlXEi__w&oe=6755F72D", use_container_width=True)
    if st.button('NRP Amanda'):
        st.write('220534025') 

with col3 :
    st.header("Widya")
    st.image("https://scontent.fbdo9-1.fna.fbcdn.net/v/t39.30808-6/468394564_122190413282168129_2674353143231961010_n.jpg?stp=dst-jpg_s600x600&_nc_cat=110&ccb=1-7&_nc_sid=833d8c&_nc_ohc=m_bbxN0rOdgQ7kNvgGQkwDN&_nc_zt=23&_nc_ht=scontent.fbdo9-1.fna&_nc_gid=A7ySlzRUjfMkZtaQxHBjRdu&oh=00_AYDEXtBK-CrLv0lYz07n-erV2cP40mKf3vvsAlja-d-X8A&oe=6755E094", use_container_width=True)
    if st.button('NRP Widya'):
        st.write('220534026') 

with col4 :
    st.header("Noviyanti")
    st.image("https://scontent.fbdo9-1.fna.fbcdn.net/v/t39.30808-6/468403667_122190413156168129_8872366674385927362_n.jpg?_nc_cat=111&ccb=1-7&_nc_sid=833d8c&_nc_ohc=jmWRtoO_ZW8Q7kNvgEdUcka&_nc_zt=23&_nc_ht=scontent.fbdo9-1.fna&_nc_gid=ARYelPnwHcYNs0AvyNWj_zD&oh=00_AYDWXPonKGarlrA4-S7SU_i0E7avNoqb-WYy8jCzD3iEwg&oe=6755E6F5", use_container_width=True)
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
