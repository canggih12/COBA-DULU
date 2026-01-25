import streamlit as st
import google.generativeai as genai

# Konfigurasi Halaman
st.set_page_config(page_title="Affiliate Genie Pro", page_icon="🪄", layout="centered")

# Custom CSS
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .result-card {
        background-color: white;
        padding: 25px;
        border-radius: 15px;
        border-left: 8px solid #FF4B4B;
        box-shadow: 0 10px 20px rgba(0,0,0,0.05);
        color: #333;
        white-space: pre-wrap;
        margin-bottom: 20px;
    }
    .stButton>button {
        border-radius: 10px;
        font-weight: bold;
        background-color: blue;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🪄 Affiliate Genie Pro")

# --- AREA INPUT ---
with st.sidebar:
    st.header("Konfigurasi API")
    api_key = st.secrets["GEMINI_API_KEY"]
    st.divider()
    st.info("Tips: Masukkan konteks spesifik agar AI tidak melantur.")

with st.container():
    produk = st.text_input("Nama Produk", placeholder="Contoh: Lampu Tidur Proyektor")
    konteks = st.text_area("Konteks/Kegunaan Spesifik", placeholder="Misal: Fokus buat kado ulang tahun anak atau buat dekorasi kamar estetik.")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        target_usia = st.selectbox("Target Usia", ["18-24 tahun", "24-35 Tahun", "35-50 Tahun", "18-45 Tahun"])
    with col2:
        durasi = st.selectbox("Durasi", ["20 detik", "30 detik", "45 detik", "60 detik"])
    with col3:
        angle = st.selectbox("Angle Konten", ["Review Jujur", "Tips & Trik", "Eksperimen", "Storytelling"])

# --- FUNGSI GENERATE ---
def generate_content():
    if not api_key or not produk:
        st.warning("Nama Produk dan API Key wajib diisi!")
        return
    
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-3-flash-preview')
        
        prompt = f"""
        Buat skrip affiliate {durasi} untuk {produk}.
        Konteks: {konteks if konteks else 'Umum'}
        Angle: {angle} | Target: {target_usia}
        
        WAJIB:
        1. Hook yang kuat di awal.
        2. Masalah & Solusi sesuai konteks.
        3. Gaya Bahasa Sesuai Dengan Target Usia
        4. CTA: "Klik keranjang di pojok kiri bawah sekarang juga!"
        5. Berikan variasi kata-kata yang berbeda dari sebelumnya.
        """
        
        with st.spinner('Meracik ide baru...'):
            response = model.generate_content(prompt)
            st.session_state.hasil_ai = response.text
    except Exception as e:
        st.error(f"Error: {e}")

# --- TOMBOL UTAMA ---
if st.button("Generate", use_container_width=True):
    generate_content()

# --- TAMPILAN HASIL ---
if 'hasil_ai' in st.session_state:
    st.markdown("---")
    st.markdown(f"### 🎬 Hasil Skrip ({angle})")
    st.markdown(f"""<div class="result-card">{st.session_state.hasil_ai}</div>""", unsafe_allow_html=True)
    
    # TOMBOL GENERATE LAGI DI BAWAH HASIL
    col_left, col_right = st.columns([1, 1])
    with col_left:
        if st.button("🔄 Coba Ide Lain", use_container_width=True):
            generate_content()
            st.rerun() # Refresh untuk menampilkan hasil baru
    with col_right:
        st.button("✅ Selesai", use_container_width=True, type="primary")
