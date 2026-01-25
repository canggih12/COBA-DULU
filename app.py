import streamlit as st
import google.generativeai as genai

# Konfigurasi Halaman
st.set_page_config(page_title="Affiliate Genie AI", page_icon="🪄", layout="centered")

# Custom CSS
st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    .stSelectbox, .stTextInput { margin-bottom: 10px; }
    .result-card {
        background-color: white;
        padding: 25px;
        border-radius: 15px;
        border-left: 8px solid #FF4B4B;
        box-shadow: 0 10px 20px rgba(0,0,0,0.05);
        line-height: 1.6;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("IDE KONTEN CUAN GENERATOR")
st.write("Sesuaikan target marketmu agar konversi makin tinggi!")

# --- AREA INPUT ---
with st.expander("⚙️ Konfigurasi Konten", expanded=True):
    api_key = "AIzaSyCaSLrhJgnx6Ok5RKItn1pCf4zyPcA45Ds"
    produk = st.text_input("Nama Produk", placeholder="------")
    
    col1, col2 = st.columns(2)
    with col1:
        target_usia = st.selectbox(
            "Target Usia Pembeli", 
            ["Remaja/Gen Z (15-24)", "Dewasa Muda (25-35)", "Orangtua (35-50)"]
        )
    with col2:
        gaya_bahasa = st.selectbox("Tone Bicara", ["Sangat Santai", "Informatif", "Emosional", "To The Point"])

# --- PROMPT LOGIC ---
if st.button("Generate Skrip Viral ✨"):
    if not api_key or not produk:
        st.warning("Lengkapi data produk dulu Ya")
    else:
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-3-flash-preview')
            
            prompt = f"""
            Tugas: Buat skrip affiliate video pendek (TikTok/Shopee).
            Produk: {produk}
            Target Usia: {target_usia}
            Gaya Bahasa: {gaya_bahasa}

            Instruksi Khusus:
            1. Sesuaikan kosa kata dengan target usia {target_usia}. Jika Gen Z gunakan bahasa gaul yang relevan. Jika Orang Tua, gunakan bahasa yang sopan dan jelas.
            2. Struktur: 
               - HOOK: 3 detik pertama yang bikin berhenti scroll.
               - MASALAH: Relate dengan usia tersebut.
               - SOLUSI: Manfaat {produk}.
               - CTA: Wajib sebut "Klik keranjang di pojok kiri bawah sekarang juga!".
            """
            
            with st.spinner('Menyesuaikan frekuensi bahasa AI...'):
                response = model.generate_content(prompt)
                
                st.markdown("### 🎬 Skrip Konten Kamu")
                st.markdown(f"""<div class="result-card">{response.text}</div>""", unsafe_allow_html=True)
                st.balloons()
                
        except Exception as e:
            st.error(f"Error: {e}")

st.markdown("---")
st.caption("Tips: Untuk target Gen Z, jangan terlalu kaku. Untuk Orang Tua, fokus pada solusi masalah sehari-hari.")
