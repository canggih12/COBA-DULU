import streamlit as st
import google.generativeai as genai

# Konfigurasi Halaman
st.set_page_config(page_title="Affiliate Genie Pro", page_icon="🪄", layout="centered")

# --- FUNGSI RESET ---
def reset_form():
    st.session_state["produk"] = ""
    st.session_state["konteks"] = ""
    st.session_state["sudah_klik"] = False
    if "hasil_ai" in st.session_state:
        del st.session_state["hasil_ai"]

# --- SETUP API KEY ---
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-3-flash-preview')
except:
    st.error("API Key belum disetting di Secrets!")

# --- CUSTOM CSS UNTUK WARNA TOMBOL ---
if "sudah_klik" not in st.session_state:
    st.session_state["sudah_klik"] = False

# Logika warna tombol Generate (Berubah saat diklik)
gen_bg = "#E74C3C" if st.session_state["sudah_klik"] else "#3498DB"
gen_txt = "#000000" if st.session_state["sudah_klik"] else "#FFFFFF"

st.markdown(f"""
    <style>
    /* 1. Tombol Generate (Biru -> Merah) */
    div.stButton > button:first-child {{
        background-color: {gen_bg} !important;
        color: {gen_txt} !important;
        border-radius: 10px; font-weight: bold; height: 3.5em; width: 100%; border: none;
    }}
    
    /* 2. Tombol Coba Ide Lain (Kuning/Orange) */
    div.stButton > button[key="btn_lagi"] {{
        background-color: #F39C12 !important;
        color: white !important;
        border-radius: 10px; font-weight: bold; border: none;
    }}
    
    /* 3. Tombol Selesai (Hijau) */
    div.stButton > button[key="btn_selesai"] {{
        background-color: #27AE60 !important;
        color: white !important;
        border-radius: 10px; font-weight: bold; border: none;
    }}

    .box-container {{
        background-color: white; padding: 15px; border-radius: 10px;
        border: 2px solid #333; margin-bottom: 20px;
    }}
    .label-box {{ font-weight: bold; margin-bottom: 5px; display: block; }}
    </style>
    """, unsafe_allow_html=True)

st.title("🪄 Affiliate Genie Pro")

# --- INPUT AREA ---
produk = st.text_input("Nama Produk", key="produk")
konteks = st.text_area("Konteks / Situasi", key="konteks")

col1, col2, col3 = st.columns(3)
with col1:
    target_usia = st.selectbox("Target Usia", ["Gen Z", "Dewasa", "Orang Tua", "Umum"])
with col2:
    durasi = st.selectbox("Durasi", ["20 detik", "30 detik", "45 detik", "60 detik"])
with col3:
    angle = st.selectbox("Angle", ["Review Jujur", "Tips & Trik", "Eksperimen", "Storytelling"])

# --- GENERATE LOGIC ---
def generate_content():
    if not produk:
        st.warning("Isi nama produk!")
        return
    st.session_state["sudah_klik"] = True
    try:
        prompt = f"Buat skrip affiliate {durasi} untuk {produk}. Konteks: {konteks}. Angle: {angle}. Pisahkan Visual dan Voice Over."
        response = model.generate_content(prompt)
        st.session_state.hasil_ai = response.text
    except:
        st.error("Gagal generate!")

st.button("Generate Skrip Viral ✨", on_click=generate_content)

# --- TAMPILAN HASIL ---
if 'hasil_ai' in st.session_state:
    st.markdown("---")
    
    # Visual Box
    st.markdown("<span class='label-box'>visual konten</span>", unsafe_allow_html=True)
    st.markdown(f"<div class='box-container'>{st.session_state.hasil_ai}</div>", unsafe_allow_html=True)

    # Voice Over Box (Copyable)
    st.markdown("<span class='label-box'>teks voice over</span>", unsafe_allow_html=True)
    st.code(st.session_state.hasil_ai, language="text")

    # Tombol Navigasi dengan Warna Berbeda
    col_re, col_done = st.columns(2)
    with col_re:
        if st.button("🔄 Coba Ide Lain", key="btn_lagi", use_container_width=True):
            generate_content()
            st.rerun()
    with col_done:
        if st.button("✅ Selesai & Reset", key="btn_selesai", use_container_width=True, on_click=reset_form):
            st.rerun()
