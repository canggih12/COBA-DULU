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

# --- DYNAMIC CSS ---
if "sudah_klik" not in st.session_state:
    st.session_state["sudah_klik"] = False

# Logika Warna Tombol
btn_bg = "#E74C3C" if st.session_state["sudah_klik"] else "#3498DB"  # Merah jika sudah, Biru jika belum
btn_txt = "#000000" if st.session_state["sudah_klik"] else "#FFFFFF" # Hitam jika sudah, Putih jika belum

st.markdown(f"""
    <style>
    .stButton>button {{
        background-color: {btn_bg} !important;
        color: {btn_txt} !important;
        border-radius: 10px;
        font-weight: bold;
        transition: 0.3s;
        border: none;
        height: 3em;
        width: 100%;
    }}
    .vo-card {{
        background-color: #f0f7ff; padding: 20px; border-radius: 12px;
        border-left: 5px solid #3498db; margin-bottom: 15px;
    }}
    .visual-card {{
        background-color: #fff5f5; padding: 20px; border-radius: 12px;
        border-left: 5px solid #e74c3c;
    }}
    .label-tag {{
        font-weight: bold; text-transform: uppercase; font-size: 0.8em; margin-bottom: 5px; display: block;
    }}
    </style>
    """, unsafe_allow_html=True)

st.title("🪄 Affiliate Genie Pro")

# --- AREA INPUT ---
with st.container():
    produk = st.text_input("Nama Produk", key="produk", placeholder="Contoh: Blender Portable")
    konteks = st.text_area("Konteks/Kegunaan Spesifik", key="konteks", placeholder="Misal: Fokus buat bikin smoothie di kantor.")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        target_usia = st.selectbox("Target Usia", ["Gen Z", "Dewasa", "Orang Tua", "Umum"])
    with col2:
        durasi = st.selectbox("Durasi", ["20 detik", "30 detik", "45 detik", "60 detik"])
    with col3:
        angle = st.selectbox("Angle", ["Review Jujur", "Tips & Trik", "Eksperimen", "Storytelling"])

# --- FUNGSI GENERATE ---
def generate_content():
    if not produk:
        st.warning("Nama Produk wajib diisi!")
        return
    
    st.session_state["sudah_klik"] = True
    try:
        prompt = f"""Buat skrip affiliate {durasi} untuk {produk}. Konteks: {konteks}. 
        Angle: {angle} | Target: {target_usia}.
        
        Pisahkan output menjadi 2 bagian:
        1. VOICE OVER: Berisi narasi teks yang harus dibacakan (bahasa santai/relate).
        2. VISUAL: Berisi instruksi apa yang harus direkam/ditampilkan di layar.
        
        WAJIB CTA di akhir Voice Over: "Klik keranjang di pojok kiri bawah sekarang juga!"."""
        
        with st.spinner('Meracik ide...'):
            response = model.generate_content(prompt)
            # Logika sederhana memisahkan teks (asumsi AI memberikan pemisah)
            st.session_state.hasil_ai = response.text
    except Exception as e:
        st.error(f"Error: {e}")

# Tombol Generate
st.button("Generate Skrip Viral ✨", on_click=generate_content)

# --- TAMPILAN HASIL ---
if 'hasil_ai' in st.session_state:
    st.markdown("---")
    st.markdown("### 🎬 Blueprint Konten Kamu")
    
    # Menampilkan hasil AI dalam struktur yang rapi
    # Kita bagi dua kolom atau dua baris sesuai permintaanmu
    st.markdown(f"""
    <div class="vo-card">
        <span class="label-tag" style="color: #3498db;">🎙️ Voice Over / Script (Suara)</span>
        {st.session_state.hasil_ai.split('VISUAL')[0].replace('VOICE OVER:', '')}
    </div>
    
    <div class="visual-card">
        <span class="label-tag" style="color: #e74c3c;">📸 Panduan Visual (Gambar/Video)</span>
        {"VISUAL" + st.session_state.hasil_ai.split('VISUAL')[-1] if 'VISUAL' in st.session_state.hasil_ai else "Instruksi visual menyesuaikan narasi di atas."}
    </div>
    """, unsafe_allow_html=True)
    
    col_re, col_done = st.columns(2)
    with col_re:
        if st.button("🔄 Coba Ide Lain", use_container_width=True):
            generate_content()
            st.rerun()
    with col_done:
        if st.button("✅ Selesai & Input Baru", use_container_width=True, type="primary", on_click=reset_form):
            st.rerun()
