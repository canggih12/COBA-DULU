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
        white-space: pre-wrap; /* Menjaga Enter dari AI tetap muncul */
        word-wrap: break-word;
    }}
    
    .label-box {{ 
        font-weight: bold; 
        text-transform: uppercase; 
        font-size: 0.85em; 
        margin-bottom: 8px; 
        display: block; 
        color: #444; 
    }}

    div.stButton > button:first-child {{
        background-color: {gen_bg} !important;
        color: {gen_txt} !important;
        border-radius: 10px; font-weight: bold; height: 3.5em; width: 100%; border: none;
    }}
    div.stButton > button[key="btn_lagi"] {{
        background-color: #F39C12 !important; color: white !important;
        border-radius: 10px; font-weight: bold; border: none;
    }}
    div.stButton > button[key="btn_selesai"] {{
        background-color: #27AE60 !important; color: white !important;
        border-radius: 10px; font-weight: bold; border: none;
    }}
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
        # Prompt dipertegas untuk pemisahan baris per durasi
        prompt = f"""Buat skrip affiliate {durasi} untuk {produk}. Konteks: {konteks}. Target Usia: {Terget_Usia}. Angle: {angle}.
        Wajib gunakan format list vertikal ke bawah seperti ini:

        BAGIAN VISUAL:
        0-5 detik: (instruksi)
        5-10 detik: (instruksi)
        dst...

        ---

        BAGIAN VOICE OVER:
        0-5 detik (Hook): (teks narasi)
        5-10 detik: (teks narasi)
        dst...

        Jangan gunakan tabel. Berikan enter (jarak baris) yang jelas antar durasi."""
        
        response = model.generate_content(prompt)
        st.session_state.hasil_ai = response.text
    except:
        st.error("Gagal generate!")

st.button("Generate Skrip Viral ✨", on_click=generate_content)

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
    st.markdown("<span class='label-box'>🎙️ teks voice over</span>", unsafe_allow_html=True)
    st.code(vo_text, language="text")

    # Tombol Navigasi
    col_re, col_done = st.columns(2)
    with col_re:
        if st.button("🔄 Coba Ide Lain", key="btn_lagi", use_container_width=True):
            generate_content()
            st.rerun()
    with col_done:
        if st.button("✅ Selesai & Reset", key="btn_selesai", use_container_width=True, on_click=reset_form):
            st.rerun()
