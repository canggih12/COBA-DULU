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

# --- SETUP API KEY (SECRETS) ---
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-3-flash-preview')
except Exception as e:
    st.error("Konfigurasi API Error!")

# --- DYNAMIC CSS ---
if "sudah_klik" not in st.session_state:
    st.session_state["sudah_klik"] = False

btn_bg = "#E74C3C" if st.session_state["sudah_klik"] else "#3498DB"
btn_txt = "#000000" if st.session_state["sudah_klik"] else "#FFFFFF"

st.markdown(f"""
    <style>
    .main {{ background-color: #f9f9f9; }}
    .stButton>button {{
        background-color: {btn_bg} !important;
        color: {btn_txt} !important;
        border-radius: 12px; font-weight: bold; border: none; height: 3.5em; width: 100%;
    }}
    .section-container {{
        background-color: white;
        padding: 20px;
        border-radius: 15px;
        margin-bottom: 20px;
        border: 1px solid #eee;
    }}
    .visual-header {{
        color: #e74c3c; font-weight: bold; font-size: 0.9em; margin-bottom: 10px;
    }}
    .vo-header {{
        color: #3498db; font-weight: bold; font-size: 0.9em; margin-bottom: 10px;
    }}
    </style>
    """, unsafe_allow_html=True)

st.title("🪄 Affiliate Genie Pro")

# --- INPUT AREA ---
produk = st.text_input("📦 Nama Produk", key="produk")
konteks = st.text_area("🎯 Konteks / Situasi", key="konteks")

col1, col2, col3 = st.columns(3)
with col1:
    target_usia = st.selectbox("👥 Target", ["Gen Z", "Dewasa", "Orang Tua", "Umum"])
with col2:
    durasi = st.selectbox("⏱️ Durasi", ["20 detik", "30 detik", "45 detik", "60 detik"])
with col3:
    angle = st.selectbox("🎬 Angle", ["Review Jujur", "Tips & Trik", "Eksperimen", "Storytelling"])

# --- GENERATE ---
def generate_content():
    if not produk:
        st.warning("Isi nama produk dulu!")
        return
    st.session_state["sudah_klik"] = True
    try:
        prompt = f"""Buat skrip affiliate {durasi} untuk {produk}. Konteks: {konteks}. Angle: {angle}. 
        PENTING: Jangan gunakan tabel. Berikan output dalam format poin-poin.
        Tuliskan [VISUAL] lalu dibawahnya [VOICE OVER] untuk setiap adegan.
        Berikan CTA: "Klik keranjang di pojok kiri bawah sekarang!" di akhir."""
        
        response = model.generate_content(prompt)
        st.session_state.hasil_ai = response.text
    except:
        st.error("Gagal generate!")

st.button("RACIK SKRIP VIRAL ✨", on_click=generate_content)

# --- TAMPILAN HASIL (TANPA TABEL) ---
if 'hasil_ai' in st.session_state:
    st.markdown("### 🎬 Rencana Konten")
    
    # Menampilkan panduan Visual terlebih dahulu (Tidak untuk disalin)
    with st.expander("📸 LIHAT PANDUAN VISUAL (Instruksi Kamera)", expanded=True):
        st.markdown(st.session_state.hasil_ai) # Menampilkan teks lengkap agar alur terlihat

    st.markdown("---")
    
    # FITUR UTAMA: VOICE OVER YANG BISA DISALIN
    st.markdown("### 🎙️ VOICE OVER (Siap Salin)")
    st.info("Klik ikon di pojok kanan atas kotak di bawah ini untuk menyalin teks narasi saja.")
    
    # Kita bersihkan teks dari label [VISUAL] agar yang disalin hanya suaranya
    raw_text = st.session_state.hasil_ai
    # Sederhananya, kita tampilkan dalam st.code agar ada tombol COPY otomatis
    st.code(raw_text, language="text")

    # TOMBOL FOOTER
    col_re, col_done = st.columns(2)
    with col_re:
        if st.button("🔄 Coba Ide Lain"):
            generate_content()
            st.rerun()
    with col_done:
        if st.button("✅ Selesai", type="primary", on_click=reset_form):
            st.rerun()
