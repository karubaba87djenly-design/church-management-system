import streamlit as st
import pandas as pd
import os

# Konfigurasi Halaman
st.set_page_config(page_title="Church Manager Pro", layout="wide")

# Fungsi untuk memuat data
def load_data(filename, columns):
    if os.path.exists(filename):
        return pd.read_csv(filename)
    return pd.DataFrame(columns=columns)

# Inisialisasi Data
jemaat_file = 'data_jemaat.csv'
keuangan_file = 'data_keuangan.csv'

df_jemaat = load_data(jemaat_file, ['ID', 'Nama', 'Sektor', 'Status'])
df_keuangan = load_data(keuangan_file, ['Tanggal', 'Keterangan', 'Tipe', 'Jumlah'])

# Sidebar Navigasi
menu = st.sidebar.selectbox("Menu Utama", ["Dashboard", "Data Jemaat", "Keuangan"])

if menu == "Dashboard":
    st.title("⛪ Dashboard Gereja")
    col1, col2 = st.columns(2)
    col1.metric("Total Jemaat", len(df_jemaat))
    saldo = df_keuangan[df_keuangan['Tipe'] == 'Masuk']['Jumlah'].sum() - \
            df_keuangan[df_keuangan['Tipe'] == 'Keluar']['Jumlah'].sum()
    col2.metric("Saldo Kas", f"Rp {saldo:,.0f}")

elif menu == "Data Jemaat":
    st.title("👥 Manajemen Jemaat")
    
    with st.form("form_jemaat"):
        nama = st.text_input("Nama Lengkap")
        sektor = st.selectbox("Sektor/Wilayah", ["Utara", "Selatan", "Barat", "Timur"])
        status = st.radio("Status", ["Aktif", "Pindah", "Lainnya"])
        submit = st.form_submit_button("Tambah Jemaat")
        
        if submit:
            new_data = pd.DataFrame([[len(df_jemaat)+1, nama, sektor, status]], columns=df_jemaat.columns)
            df_jemaat = pd.concat([df_jemaat, new_data], ignore_index=True)
            df_jemaat.to_csv(jemaat_file, index=False)
            st.success("Data berhasil disimpan!")

    st.dataframe(df_jemaat, use_container_width=True)

elif menu == "Keuangan":
    st.title("💰 Laporan Keuangan")
    
    with st.expander("Tambah Transaksi Baru"):
        tgl = st.date_input("Tanggal")
        ket = st.text_input("Keterangan (Contoh: Kolekte Minggu)")
        tipe = st.selectbox("Tipe", ["Masuk", "Keluar"])
        jml = st.number_input("Jumlah (Rp)", min_value=0)
        btn_keuangan = st.button("Simpan Transaksi")
        
        if btn_keuangan:
            new_trans = pd.DataFrame([[tgl, ket, tipe, jml]], columns=df_keuangan.columns)
            df_keuangan = pd.concat([df_keuangan, new_trans], ignore_index=True)
            df_keuangan.to_csv(keuangan_file, index=False)
            st.rerun()

    st.table(df_keuangan)