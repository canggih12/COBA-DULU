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
    st.error("Pastikan GEMINI_API_KEY sudah diset di Streamlit Secrets!")

# --- DYNAMIC CSS (OPTIMIZED) ---
if "sudah_klik" not in st.session_state:
    st.session_state["sudah_klik"] = False

btn_bg = "#E74C3C" if st.session_state["sudah_klik"] else "#3498DB"
btn_txt = "#000000" if st.session_state["sudah_klik"] else "#FFFFFF"

st.markdown(f"""
    <style>
    /* Mengatur Font Global */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
    html, body, [class*="st-"] {{
        font-family: 'Inter', sans-serif;
    }}
    
    /* Main Container */
    .main {{ background-color: #fcfcfc; }}
    
    /* Tombol Utama */
    .stButton>button {{
        background-color: {btn_bg} !important;
        color: {btn_txt} !important;
        border-radius: 12px;
        font-weight: 800;
        letter-spacing: 0.5px;
        transition: all 0.3s ease;
        border: none;
        height: 3.5em;
        width: 100%;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }}
    
    /* Kartu Output Voice Over */
    .vo-card {{
        background-color: #ffffff;
        padding: 25px;
        border-radius: 16px;
        border-top: 6px solid #3498db;
        box-shadow: 0 10px 30px rgba(52, 152, 219, 0.1);
        margin-bottom: 25px;
        color: #2c3e50;
    }}
    
    /* Kartu Output Visual */
    .visual-card {{
        background-color: #ffffff;
        padding: 25px;
        border-radius: 16px;
        border-top: 6px solid #e74c3c;
        box-shadow: 0 10px 30px rgba(231, 76, 60, 0.1);
        margin-bottom: 25px;
        color: #2c3e50;
    }}
    
    /* Label Tag Style */
    .label-tag {{
        display: inline-block;
        padding: 4px 12px;
        border-radius: 8px;
        font-size: 0.75em;
        font-weight: 800;
        margin-bottom: 12px;
        color: white;
    }}
    
    /* Text Area & Input Styling */
    .stTextArea textarea, .stTextInput input {{
        border-radius: 12px !important;
        border: 1px solid #e0e0e0 !important;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- UI HEADER ---
st.markdown("<h1 style='text-align: center;'>🪄 Affiliate Genie Pro</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #7f8c8d;'>Rancang konten video viral dalam hitungan detik</p>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

# --- AREA INPUT ---
with st.container():
    produk = st.text_input("📦 Nama Produk", key="produk", placeholder="Apa produk yang mau kamu jual?")
    konteks = st.text_area("🎯 Konteks / Situasi", key="konteks", placeholder="Ceritakan situasinya (misal: buat kado, buat bersihin noda, dll)")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        target_usia = st.selectbox("👥 Target Usia", ["Gen Z", "Dewasa", "Orang Tua", "Umum"])
    with col2:
        durasi = st.selectbox("⏱️ Durasi", ["20 detik", "30 detik", "45 detik", "60 detik"])
    with col3:
        angle = st.selectbox("🎬 Angle", ["Review Jujur", "Tips & Trik", "Eksperimen", "Storytelling"])

st.markdown("<br>", unsafe_allow_html=True)

# --- LOGIKA GENERATE ---
def generate_content():
    if not produk:
        st.warning("Nama Produk wajib diisi!")
        return
    
    st.session_state["sudah_klik"] = True
    try:
        prompt = f"""
        Buat skrip affiliate video pendek ({durasi}) untuk produk: {produk}.
        Konteks Spesifik: {konteks}.
        Angle Konten: {angle} | Target Audiens: {target_usia}.
        
        WAJIB Pisahkan menjadi dua bagian utama:
        1. [VOICE OVER]: Narasi teks yang diucapkan. Gunakan bahasa yang {target_usia} banget. Masukkan CTA: "Klik keranjang di pojok kiri bawah sekarang!".
        2. [VISUAL]: Panduan adegan/visual per detik agar sesuai dengan narasi.
        """
        
        with st.spinner('Magic is happening...'):
            response = model.generate_content(prompt)
            st.session_state.hasil_ai = response.text
    except Exception as e:
        st.error(f"Gagal memanggil jin AI: {e}")

# Tombol Generate
st.button("RACIK SKRIP VIRAL ✨", on_click=generate_content)

# --- TAMPILAN HASIL ---
if 'hasil_ai' in st.session_state:
    st.markdown("<br><hr>", unsafe_allow_html=True)
    
    # Parsing teks (Sederhana tapi efektif)
    teks_ai = st.session_state.hasil_ai
    part_vo = teks_ai.split("[VISUAL]")[0].replace("[VOICE OVER]", "").strip()
    part_vi = teks_ai.split("[VISUAL]")[-1].strip() if "[VISUAL]" in teks_ai else "Instruksi visual akan muncul otomatis."

    # Tampilan Voice Over
    st.markdown(f"""
    <div class="vo-card">
        <span class="label-tag" style="background-color: #3498db;">🎙️ VOICE OVER</span>
        <div style="font-size: 1.1em; line-height: 1.8;">{part_vo}</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Tampilan Visual
    st.markdown(f"""
    <div class="visual-card">
        <span class="label-tag" style="background-color: #e74c3c;">📸 PANDUAN VISUAL</span>
        <div style="font-size: 1em; line-height: 1.6; color: #555;">{part_vi}</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    col_re, col_done = st.columns(2)
    with col_re:
        if st.button("🔄 Coba Ide Lain", use_container_width=True):
            generate_content()
            st.rerun()
    with col_done:
        if st.button("✅ Selesai & Reset", use_container_width=True, type="primary", on_click=reset_form):
            st.rerun()
