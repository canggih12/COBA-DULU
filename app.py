import streamlit as st
import google.generativeai as genai

# Konfigurasi Halaman
st.set_page_config(page_title="SKRIPI KONTEN", page_icon="🪄", layout="centered")

# --- FUNGSI RESET ---
def reset_form():
    st.session_state["produk"] = ""
    st.session_state["konteks"] = ""
    st.session_state["value_produk"] = "" 
    st.session_state["sudah_klik"] = False
    if "hasil_ai" in st.session_state:
        del st.session_state["hasil_ai"]

# --- SETUP API KEY ---
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-3-flash-preview')
except:
    st.error("API Key belum diset di Secrets!")

# --- CUSTOM CSS ---
if "sudah_klik" not in st.session_state:
    st.session_state["sudah_klik"] = False

gen_bg = "#E74C3C" if st.session_state["sudah_klik"] else "#3498DB"
gen_txt = "#000000" if st.session_state["sudah_klik"] else "#FFFFFF"

st.markdown(f"""
    <style>
    .box-container {{
        background-color: white; 
        padding: 20px; 
        border-radius: 12px;
        border: 2px solid #333; 
        margin-bottom: 20px; 
        color: #333;
        line-height: 1.8; 
        font-family: sans-serif;
        white-space: pre-wrap; 
        word-wrap: break-word;
    }}
    .footer {{
        position: relative;
        left: 0;
        bottom: 0;
        width: 100%;
        text-align: center;
        color: #95a5a6;
        font-size: 0.8em;
        padding: 20px 0px;
        border-top: 1px solid #eee;
        margin-top: 50px;
    }}
    .label-box {{ 
        font-weight: bold; 
        text-transform: uppercase; 
        font-size: 0.85em; 
        margin-bottom: 8px; 
        display: block; 
        color: #444; 
    }}

    /* Tombol Utama Generate */
    div.stButton > button:first-child {{
        background-color: {gen_bg} !important;
        color: {gen_txt} !important;
        border-radius: 10px; font-weight: bold; height: 3.5em; width: 100%; border: none;
    }}
    
    /* Tombol Coba Ide Lain (Sekarang warna BIRU) */
    div.stButton > button[key="btn_lagi"] {{
        background-color: #3498DB !important; color: white !important;
        border-radius: 10px; font-weight: bold; border: none;
    }}
    
    /* Tombol Reset (Tetap warna HIJAU atau bisa disesuaikan) */
    div.stButton > button[key="btn_reset"] {{
        background-color: #27AE60 !important; color: white !important;
        border-radius: 10px; font-weight: bold; border: none;
    }}
    
    .tagline {{
        color: #7f8c8d;
        font-size: 1.1em;
        text-align: center;
        margin-top: -15px;
        margin-bottom: 30px;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- UI HEADER ---
st.markdown("<h1 style='text-align: center;'>Skripi Konten</h1>", unsafe_allow_html=True)
st.markdown("<p class='tagline'>Rancang Skrip Video Viral & Auto-Cuan dalam Hitungan Detik</p>", unsafe_allow_html=True)

# --- INPUT AREA ---
produk = st.text_input("📦 Nama Produk", key="produk")
value_produk = st.text_input("💎 Keunggulan / Value Produk", key="value_produk", placeholder="Contoh: Anti air, garansi 1 thn, bahan kulit asli")
konteks = st.text_area("🎯 Konteks / Situasi", key="konteks")

col1, col2, col3 = st.columns(3)
with col1:
    target_usia = st.selectbox("👥 Target Usia", ["Gen Z", "Dewasa", "Orang Tua", "Umum"])
with col2:
    durasi = st.selectbox("⏱️ Durasi", ["20 detik", "30 detik", "45 detik", "60 detik"])
with col3:
    angle = st.selectbox("🎬 Angle Konten", ["Review Jujur", "Tips & Trik", "Eksperimen", "Storytelling"])

# --- GENERATE LOGIC ---
def generate_content():
    st.session_state["sudah_klik"] = True
    try:
        prompt = f"""Buat skrip affiliate {durasi} untuk {produk}. 
        Keunggulan Produk: {value_produk}.
        Konteks: {konteks}. 
        Target Usia: {target_usia}. 
        Angle: {angle}.
        
        PENTING: Gunakan gaya bahasa dan kosa kata yang sangat sesuai untuk {target_usia}.
        Wajib gunakan format vertikal ke bawah dengan jeda antar baris yang jelas. 
        DILARANG MENGGUNAKAN TABEL.

        Susun seperti ini:

        BAGIAN VISUAL:
        0-5 detik: [Instruksi kamera]
        
        5-10 detik: [Instruksi kamera]
        
        dst...

        ---

        BAGIAN VOICE OVER:
        0-5 detik (Hook): [Teks narasi]
        
        5-10 detik: [Teks narasi]
        
        dst...

        Berikan 1x enter (baris kosong) antar segmen waktu agar rapi."""
        
        response = model.generate_content(prompt)
        st.session_state.hasil_ai = response.text
    except:
        st.error("Gagal generate!")

# Tombol Generate
if st.button("Generate Skrip"):
    if not produk:
        st.warning("⚠️ Nama Produk wajib diisi!")
    else:
        generate_content()

# --- TAMPILAN HASIL ---
if 'hasil_ai' in st.session_state:
    st.markdown("---")
    
    res = st.session_state.hasil_ai
    if "---" in res:
        parts = res.split("---")
        visual_text = parts[0].replace("BAGIAN VISUAL:", "").strip()
        vo_text = parts[1].replace("BAGIAN VOICE OVER:", "").strip()
    else:
        visual_text = res
        vo_text = res

    # Kotak Visual
    st.markdown("<span class='label-box'>📸 visual konten</span>", unsafe_allow_html=True)
    st.markdown(f"<div class='box-container'>{visual_text}</div>", unsafe_allow_html=True)

    # Kotak Voice Over
    st.markdown("<span class='label-box'>🎙️ teks voice over (salin disini)</span>", unsafe_allow_html=True)
    st.code(vo_text, language="text")

    # Tombol Navigasi (Warna dan Nama Baru)
    col_re, col_done = st.columns(2)
    with col_re:
        if st.button("🔄 Coba Ide Lain", key="btn_lagi", use_container_width=True):
            generate_content()
            st.rerun()
    with col_done:
        # Nama diganti jadi Reset, fungsi reset_form tetap dipertahankan
        if st.button("🗑️ Reset", key="btn_reset", use_container_width=True, on_click=reset_form):
            st.rerun()
            # --- FOOTER (NAMA PEMBUAT) ---
st.markdown("""
    <div class="footer">
        <p>Built with ❤️ by <b>[Cerita Ozi]</b> | © 2026 Skripi Konten Team</p>
    </div>
    """, unsafe_allow_html=True)
