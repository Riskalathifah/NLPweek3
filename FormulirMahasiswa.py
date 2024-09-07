import streamlit as st
import pandas as pd
import re
from io import StringIO
from datetime import datetime

# Set page configuration
st.set_page_config(
    page_title="Form Data Mahasiswa Unair",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS to improve UI
st.markdown("""
<style>
    .reportview-container {
        background: #f0f2f6
    }
    .sidebar .sidebar-content {
        background: #e6e9ef
    }
    .Widget>label {
        color: #31333F;
        font-weight: bold;
    }
    .stButton>button {
        color: #ffffff;
        background-color: #0066cc;
        border-radius: 5px;
    }
    .stTextInput>div>div>input {
        border-radius: 5px;
    }
    .title-container {
        display: flex;
        align-items: center;
        justify-content: center;
    }
    .logo-img {
        max-width: 100px;
        margin-right: 20px;
    }
    .custom-title {
        font-size: 24px;
        font-weight: bold;
        color: #0066cc;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state for storing form entries and form state
if 'form_entries' not in st.session_state:
    st.session_state.form_entries = []
if 'form_state' not in st.session_state:
    st.session_state.form_state = {}

# Function for input validation
def validate_input(value, pattern, message):
    if not re.match(pattern, value):
        return False
    return True

# Function to create CSV
def get_csv():
    df = pd.DataFrame(st.session_state.form_entries)
    return df.to_csv(index=False).encode('utf-8')

# Custom title with logo
def custom_title():
    title_col1, title_col2 = st.columns([1, 4])
    with title_col1:
        st.image("logounair.png", width=100)
    with title_col2:
        st.markdown("<h1 class='custom-title'>Formulir Data Diri Mahasiswa Universitas Airlangga</h1>", unsafe_allow_html=True)
    st.markdown("<hr>", unsafe_allow_html=True)

# Main form page
def form_page():
    custom_title()
    
    # Use columns for better layout
    col1, col2 = st.columns(2)
    
    fields = {
        "Nama": (r"^[a-zA-Z\s]+$", "Nama hanya boleh mengandung huruf dan spasi."),
        "Email": (r"^[a-zA-Z0-9_.+-]+(\.[a-zA-Z0-9_.+-]+)*-\d{4}@[a-zA-Z]{1,4}\.unair\.ac\.id$", "Email harus sesuai format: nama-depan.nama-belakang-tahun@fakultas.unair.ac.id"),
        "Tanggal Lahir": (r"^(0[1-9]|[12][0-9]|3[01])/(0[1-9]|1[0-2])/\d{4}$", "Format: DD/MM/YYYY"),
        "Kodepos": (r"^\d{5}$", "Harus 5 digit angka."),
        "NIM": (r"^\d{9}$", "Harus 9 digit angka."),
        "NIK": (r'^\d{6}(?:[0-2][0-9]|3[0-1]|4[1-9]|5[0-9]|6[0-9]|7[0-1])(?:0[1-9]|1[0-2])\d{2}\d{4}$', "Harus 16 digit angka."),
        "Akun Instagram": (r'^[@][a-zA-Z0-9]{3,20}$', "Diawali dengan @ dan maksimal 20 karakter."),
        "Angkatan": (r'^(195[4-9]|19[6-9]\d|200\d|201\d|202[0-4])$', "Tahun 4 digit (1954-2024)."),
        "Plat Nomor Kendaraan": (r"^[A-Z]{1,2}\s\d{1,4}\s[A-Z]{1,3}$", "Contoh: B 1234 CDE"),
        "Nomor SIM": (r"^\d{14}$", "Harus 14 digit angka."),
        "No. Telp": (r"^(?:\+62\d{9,12}|08\d{8,11})$", "Format: +62 atau 08 diikuti 9-12 angka."),
        "IPK": (r"^[0-3]\.\d{2}$|^4\.00$", "Antara 0.00 dan 4.00 dengan dua desimal."),
        "Passport": (r"^[A-Z]{1}\d{8}$", "1 huruf diikuti 8 digit angka.")
    }

    user_data = {}
    for i, (field, (pattern, message)) in enumerate(fields.items()):
        with col1 if i % 2 == 0 else col2:
            value = st.text_input(field, value=st.session_state.form_state.get(field, ""), help=message)
            st.session_state.form_state[field] = value
            if value:
                if validate_input(value, pattern, message):
                    user_data[field] = value
                else:
                    st.error(message)

    with st.expander("Alamat", expanded=False):
        alamat = st.text_area("Masukkan alamat lengkap", value=st.session_state.form_state.get("Alamat", ""))
        st.session_state.form_state["Alamat"] = alamat
        if alamat:
            user_data["Alamat"] = alamat

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Submit", key="submit"):
            if len(user_data) == len(fields) + 1:  # +1 for Alamat
                user_data["Timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                st.session_state.form_entries.append(user_data)
                st.success("Data telah berhasil disimpan!")
                st.session_state.form_state = {}  # Clear form after successful submission
            else:
                st.warning("Mohon isi semua data dengan benar.")
    with col2:
        if st.button("Clear Form"):
          st.session_state.form_state = {}
          st.session_state.clear()
          st.warning("Form has been cleared. Please refresh the page manually to reset everything.")


    with col3:
        if st.button("Lihat Data Terakhir"):
            if st.session_state.form_entries:
                st.json(st.session_state.form_entries[-1])
            else:
                st.info("Belum ada data yang dimasukkan.")

# Data view page
def data_view_page():
    custom_title()
    st.subheader("📊 Data Mahasiswa yang Telah Dimasukkan")

    if not st.session_state.form_entries:
        st.info("Belum ada data yang dimasukkan.")
    else:
        df = pd.DataFrame(st.session_state.form_entries)
        
        # Add search and filter functionality
        col1, col2 = st.columns(2)
        with col1:
            search = st.text_input("🔍 Cari Data", "")
        with col2:
            filter_column = st.selectbox("Filter berdasarkan:", ["Semua"] + list(df.columns))
        
        if search:
            if filter_column == "Semua":
                df = df[df.apply(lambda row: row.astype(str).str.contains(search, case=False).any(), axis=1)]
            else:
                df = df[df[filter_column].astype(str).str.contains(search, case=False)]
        
        st.dataframe(df)

        col1, col2, col3 = st.columns(3)
        with col1:
            csv = get_csv()
            st.download_button(
                label="📥 Download data as CSV",
                data=csv,
                file_name="data_mahasiswa_unair.csv",
                mime="text/csv",
            )
        with col2:
            if st.button("🗑️ Hapus Semua Data"):
                st.session_state.form_entries = []
                st.experimental_rerun()
        with col3:
            if st.button("📊 Statistik Data"):
                st.write("Jumlah entri:", len(df))
                st.write("Rata-rata IPK:", df["IPK"].astype(float).mean())
                st.write("Distribusi Angkatan:")
                st.bar_chart(df["Angkatan"].value_counts())

# Main app
def main():
    st.sidebar.title("📌 Navigasi")
    page = st.sidebar.radio("Pilih Halaman:", ["Form Input", "Lihat Data"])

    if page == "Form Input":
        form_page()
    elif page == "Lihat Data":
        data_view_page()

if __name__ == "__main__":
    main()
